import cv2
import os
import torch
from ultralytics import YOLO
import numpy as np
from PIL import Image 

def run_yolo_background_removal(input_video: str, output_folder: str, bg_type: str, bg_color: tuple = (0, 255, 0), bg_image_path: str = None, progress_callback=None):
    try:
        os.makedirs(output_folder, exist_ok=True)

        # You can switch to 'yolov8x-seg.pt' if you have a powerful GPU and need maximum accuracy
        model = YOLO('yolov8n-seg.pt')
        # Determine device to use (GPU if available, otherwise CPU)
        device = 0 if torch.cuda.is_available() else 'cpu'
        print(f"[INFO] Using device: {device}")

        # Load the video using OpenCV
        cap = cv2.VideoCapture(input_video)
        if not cap.isOpened():
            print(f"[ERROR] Could not open video file: {input_video}")
            return False

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Initialize VideoWriter to save output video
        base_name = os.path.splitext(os.path.basename(input_video))[0]
        output_filename = f"{base_name}_{bg_type}_bg.mp4"
        output_path = os.path.join(output_folder, output_filename)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Codec for .mp4 format

        # Check if frame dimensions are valid before creating VideoWriter
        if frame_width <= 0 or frame_height <= 0:
             print(f"[ERROR] Invalid frame dimensions: {frame_width}x{frame_height}")
             cap.release()
             return False

        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
        if not out.isOpened():
             print(f"[ERROR] Could not create video writer for path: {output_path}")
             cap.release()
             return False

        # --- Prepare Background based on Type ---
        background_image = None
        if bg_type == 'image':
            if not bg_image_path or not os.path.exists(bg_image_path):
                print(f"[ERROR] Background image not found: {bg_image_path}")
                cap.release()
                out.release()
                return False
            try:
                # Load image using PIL for better format support, then convert to OpenCV format
                bg_img_pil = Image.open(bg_image_path).convert('RGB')
                background_image = cv2.cvtColor(np.array(bg_img_pil), cv2.COLOR_RGB2BGR)
                # Resize background image to match video frame size
                background_image = cv2.resize(background_image, (frame_width, frame_height))
            except Exception as e:
                print(f"[ERROR] Could not load or process background image: {e}")
                cap.release()
                out.release()
                return False
            
        elif bg_type == 'color':
            bgr_color = (bg_color[2], bg_color[1], bg_color[0])
            background_image = np.full((frame_height, frame_width, 3), bgr_color, dtype=np.uint8)
            
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break # End of video

            frame_count += 1

            # YOLOv8 Segmentation
            # classes=[0] filters for 'person' class
            # conf=0.4 sets confidence threshold
            results = model.predict(source=frame, device=device, classes=[0], conf=0.4, verbose=False)
            masks = results[0].masks # Get masks for detected objects

            final_frame = frame.copy()

            if masks is not None and len(masks.data) > 0:
                mask = masks.data[0].cpu().numpy() 
                mask = (mask * 255).astype("uint8")
                if mask.shape[0] != frame_height or mask.shape[1] != frame_width:
                     mask = cv2.resize(mask, (frame_width, frame_height), interpolation=cv2.INTER_NEAREST)

                # Create 3-channel masks for bitwise operations
                mask_3ch = cv2.merge([mask, mask, mask])
                inverse_mask = cv2.bitwise_not(mask)
                inverse_mask_3ch = cv2.merge([inverse_mask, inverse_mask, inverse_mask])

                # Apply the mask to get the foreground (person)
                masked_person = cv2.bitwise_and(frame, mask_3ch)
                
                if bg_type == 'color' or bg_type == 'image':
                    background = cv2.bitwise_and(background_image, inverse_mask_3ch)
                    final_frame = cv2.add(masked_person, background)

                elif bg_type == 'blur':
                    blurred_frame = cv2.GaussianBlur(frame, (99, 99), 0) 
                    blurred_background = cv2.bitwise_and(blurred_frame, inverse_mask_3ch)
                    final_frame = cv2.add(masked_person, blurred_background)

            # Write the processed frame to the output video
            out.write(final_frame)

            if progress_callback:
                progress = frame_count / total_frames
                progress_callback(progress)

        cap.release()
        out.release()

        print(f"[INFO] Video processing complete. Output saved to: {output_path}")
        return True 

    except Exception as e:
        print(f"[ERROR] An error occurred during video processing: {e}")
        if 'cap' in locals() and cap.isOpened():
            cap.release()
        if 'out' in locals() and out.isOpened():
            out.release()
        return False 


