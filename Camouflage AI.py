import customtkinter as ctk
from tkinter import filedialog, colorchooser, messagebox
import os
import subprocess
import sys
import threading
from process_video import run_yolo_background_removal 

class CamouflageApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Camouflage AI")
        self.geometry("600x650")
        self.resizable(False, False)

        # --- Instance Variables ---
        self.bg_type = ctk.StringVar(value="color")
        self.bg_color_rgb = (0, 255, 0)  # Default green
        self.bg_color_hex = "#00FF00"  # Default green
        self.bg_image_path = ctk.StringVar(value="")
        self.video_path = ctk.StringVar(value="")

        # Variable to store the blur label
        self.blur_label = None

        # --- GUI Elements ---
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="#3498db", corner_radius=10)
        header_frame.pack(pady=20, padx=20, fill="x")

        title_label = ctk.CTkLabel(header_frame, text="Camouflage AI", text_color="white", font=("Segoe UI", 28, "bold"))
        title_label.pack(pady=(10, 5))

        subtitle_label = ctk.CTkLabel(header_frame, text="AI VIDEO BACKGROUND REMOVER", text_color="white", font=("Segoe UI", 16))
        subtitle_label.pack(pady=(0, 15))

        # Video selection
        self.select_video_btn = ctk.CTkButton(self, text="Select Video", command=self.select_video, font=("Segoe UI", 18), height=50, width=250, corner_radius=25, fg_color="#8e44ad")
        self.select_video_btn.pack(pady=(10, 5))
        self.video_path_label = ctk.CTkLabel(self, text="No video selected.", font=("Segoe UI", 12), wraplength=580)
        self.video_path_label.pack(pady=(0,10))

        # Background Type Selection Frame
        self.bg_selection_frame = ctk.CTkFrame(self)
        self.bg_selection_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(self.bg_selection_frame, text="Background Type:", font=("Segoe UI", 16, "bold")).pack(side="left", padx=(5,15), pady=5)

        # Radio buttons for background type
        self.rb_color = ctk.CTkRadioButton(self.bg_selection_frame, text="Color", variable=self.bg_type, value="color", command=self.on_bg_type_selected, font=("Segoe UI", 14))
        self.rb_color.pack(side="left", padx=10, pady=5)

        self.rb_image = ctk.CTkRadioButton(self.bg_selection_frame, text="Image", variable=self.bg_type, value="image", command=self.on_bg_type_selected, font=("Segoe UI", 14))
        self.rb_image.pack(side="left", padx=10, pady=5)

        self.rb_blur = ctk.CTkRadioButton(self.bg_selection_frame, text="Blur", variable=self.bg_type, value="blur", command=self.on_bg_type_selected, font=("Segoe UI", 14))
        self.rb_blur.pack(side="left", padx=10, pady=5)

        # Background Controls Frame (for color picker/image selector)
        self.bg_controls_frame = ctk.CTkFrame(self)
        self.bg_controls_frame.pack(pady=10, padx=20, fill="x", ipady=5)

        # Controls for background 
        self.select_color_btn = ctk.CTkButton(self.bg_controls_frame, text="Choose Color", command=self.choose_color, font=("Segoe UI", 16), height=40, width=200, corner_radius=20, fg_color="#2980b9")
        self.bg_color_display = ctk.CTkFrame(self.bg_controls_frame, width=40, height=40, border_width=2, corner_radius=5)

        self.select_image_btn = ctk.CTkButton(self.bg_controls_frame, text="Select Image", command=self.select_background_image, font=("Segoe UI", 16), height=40, width=200, corner_radius=20, fg_color="#27ae60")
        self.bg_image_label = ctk.CTkLabel(self.bg_controls_frame, text="No image selected.", font=("Segoe UI", 12), wraplength=350)

        # Processing and Output Buttons
        self.process_btn = ctk.CTkButton(self, text="Start Processing", command=self.start_processing_thread, font=("Segoe UI", 18, "bold"), height=50, width=250, corner_radius=25, fg_color="#c0392b", hover_color="#e74c3c")
        self.process_btn.pack(pady=(20,10))

        self.open_output_btn = ctk.CTkButton(self, text="Show Output Folder", command=self.open_output_folder, font=("Segoe UI", 16), height=40, width=220, corner_radius=20, fg_color="#7f8c8d")
        self.open_output_btn.pack(pady=5)


        self.status_label = ctk.CTkLabel(self, text="Status: Waiting for video...", font=("Segoe UI", 14), wraplength=580)
        self.status_label.pack(pady=(10, 5))

        # Footer
        footer_label = ctk.CTkLabel(self, text="Built by 💖 Vishnu | Camouflage AI", font=("Segoe UI", 14), text_color="#7f8c8d")
        footer_label.pack(pady=(15,10), side="bottom")

        # Initial setup for conditional UI elements based on default bg_type
        self.on_bg_type_selected()

    def on_bg_type_selected(self):
        selected_type = self.bg_type.get()

        # First, hide all conditional controls within the frame
        self.select_color_btn.pack_forget()
        self.bg_color_display.pack_forget()
        self.select_image_btn.pack_forget()
        self.bg_image_label.pack_forget()

        # Forget the blur label if it exists
        if self.blur_label is not None:
            self.blur_label.pack_forget()

        if selected_type == "color":
            self.select_color_btn.pack(side="left", padx=(0, 10), pady=10)
            self.bg_color_display.configure(fg_color=self.bg_color_hex)
            self.bg_color_display.pack(side="left", padx=(0, 0), pady=10)
            self.status_label.configure(text=f"Background: Color. Current: {self.bg_color_hex}", text_color="gray")

        elif selected_type == "image":
            self.select_image_btn.pack(side="left", padx=(0,10), pady=10)
            self.bg_image_label.pack(side="left", padx=(0,0), pady=10, expand=True, fill="x")
            if self.bg_image_path.get():
                self.bg_image_label.configure(text=f"{os.path.basename(self.bg_image_path.get())}")
            else:
                self.bg_image_label.configure(text="No image selected.")
            self.status_label.configure(text="Background: Image. Select an image.", text_color="gray")

        elif selected_type == "blur":
            if self.blur_label is None:
                 self.blur_label = ctk.CTkLabel(self.bg_controls_frame, text="Blur effect will be applied to the background", font=("Segoe UI", 14))
            self.blur_label.pack(pady=10, padx=10)
            self.status_label.configure(text="Background: Blur. The video's background will be blurred.", text_color="gray")


    def select_video(self):
        path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv"), ("All files", "*.*")]
        )
        if path:
            self.video_path.set(path)
            self.video_path_label.configure(text=f"{os.path.basename(path)}")
            try:
                file_size_mb = os.path.getsize(path) / (1024 * 1024)
                if file_size_mb > 200:
                    self.status_label.configure(text=f"⚠️ WARNING: Large file ({file_size_mb:.2f} MB). Processing may be slow.", text_color="orange")
                else:
                    self.status_label.configure(text=f"Video selected. Ready to set background type.", text_color="gray")
            except OSError:
                    self.status_label.configure(text=f"Video selected. Could not get file size.", text_color="gray")


    def choose_color(self):
        try:
            chosen_color = colorchooser.askcolor(title="Choose Background Color", initialcolor=self.bg_color_hex)
            if chosen_color and chosen_color[0] and chosen_color[1]:
                self.bg_color_rgb = tuple(map(int, chosen_color[0]))
                self.bg_color_hex = chosen_color[1]
                self.bg_color_display.configure(fg_color=self.bg_color_hex)
                self.status_label.configure(text=f"Background color set to: {self.bg_color_hex}", text_color="gray")
        except Exception as e:
            messagebox.showerror("Color Chooser Error", f"Could not open color chooser: {e}")


    def select_background_image(self):
        path = filedialog.askopenfilename(
            title="Select Background Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png"), ("All files", "*.*")]
        )
        if path:
            self.bg_image_path.set(path)
            self.bg_image_label.configure(text=f"{os.path.basename(path)}")
            self.status_label.configure(text=f"Background image selected: {os.path.basename(path)}", text_color="gray")

    def open_output_folder(self):
        output_folder = "output_videos"
        os.makedirs(output_folder, exist_ok=True)
        abs_path = os.path.abspath(output_folder)
        try:
            if os.name == 'nt':
                subprocess.Popen(f'explorer "{abs_path}"')
            elif os.name == 'posix':
                if sys.platform == "darwin":
                    subprocess.Popen(['open', abs_path])
                else:
                    subprocess.Popen(['xdg-open', abs_path])
            else:
                messagebox.showinfo("Open Folder", f"Please open this folder manually: {abs_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open output folder: {e}\nPath: {abs_path}")

    def set_ui_state(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self.select_video_btn.configure(state=state)
        if hasattr(self, 'rb_color'): self.rb_color.configure(state=state)
        if hasattr(self, 'rb_image'): self.rb_image.configure(state=state)
        if hasattr(self, 'rb_blur'): self.rb_blur.configure(state=state)

        # Check if controls exist before configuring state
        if hasattr(self, 'select_color_btn'): self.select_color_btn.configure(state=state)
        if hasattr(self, 'select_image_btn'): self.select_image_btn.configure(state=state)

        self.process_btn.configure(state=state)

    def update_progress_bar(self, percentage):
        if hasattr(self, 'progress_bar_instance') and self.progress_bar_instance and self.progress_bar_instance.winfo_exists():
            self.progress_bar_instance.set(float(percentage))
            if hasattr(self, 'progress_window') and self.progress_window.winfo_exists():
                self.progress_window.update_idletasks()

    def start_processing_thread(self):
        if not self.video_path.get():
            messagebox.showerror("Error", "Please select a video file first!")
            return

        if self.bg_type.get() == "image" and not self.bg_image_path.get():
            messagebox.showerror("Error", "Background type is 'Image', but no image has been selected.")
            return

        self.set_ui_state(False)
        self.status_label.configure(text="🔄 Processing... This may take a while. Please wait.", text_color="orange")

        self.progress_window = ctk.CTkToplevel(self)
        self.progress_window.title("Processing...")
        self.progress_window.geometry("400x150")
        self.progress_window.transient(self)
        self.progress_window.grab_set()
        self.progress_window.protocol("WM_DELETE_WINDOW", lambda: None)

        ctk.CTkLabel(self.progress_window, text="Video processing in progress...", font=("Segoe UI", 16)).pack(pady=(20,10))
        self.progress_bar_instance = ctk.CTkProgressBar(self.progress_window, orientation="horizontal", width=360)
        self.progress_bar_instance.pack(pady=(0,20))
        self.progress_bar_instance.set(0)

        thread = threading.Thread(target=self.process_video_actual_task, daemon=True)
        thread.start()

    def process_video_actual_task(self):
        output_folder = "output_videos"
        os.makedirs(output_folder, exist_ok=True)
        success = False
        error_message = ""
        try:
            current_bg_image_path = None
            if self.bg_type.get() == "image" and self.bg_image_path.get():
                current_bg_image_path = self.bg_image_path.get()

            success = run_yolo_background_removal(
                input_video=self.video_path.get(),
                output_folder=output_folder,
                bg_type=self.bg_type.get(),
                bg_color=self.bg_color_rgb,
                bg_image_path=current_bg_image_path,
                progress_callback=self.update_progress_bar
            )
        except Exception as e:
            print(f"Exception during video processing: {e}")
            error_message = str(e)
            success = False

        self.after(0, self.on_processing_complete, success, error_message)

    def on_processing_complete(self, success, error_message):
        if hasattr(self, 'progress_bar_instance') and self.progress_bar_instance and self.progress_bar_instance.winfo_exists():
            self.progress_bar_instance.set(1.0)

        if success:
            self.status_label.configure(text="✅ Processing complete! Output saved in 'output_videos' folder.", text_color="green")
            messagebox.showinfo("Success", "Video processing completed successfully!")
        else:
            final_error_message = "Processing failed."
            if error_message:
                final_error_message += f"\nDetails: {error_message}"
            self.status_label.configure(text=f"❌ {final_error_message}", text_color="red")
            messagebox.showerror("Error", final_error_message)

        if hasattr(self, 'progress_window') and self.progress_window.winfo_exists():
            self.progress_window.grab_release()
            self.progress_window.destroy()

        self.set_ui_state(True)


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = CamouflageApp()
    app.mainloop()
