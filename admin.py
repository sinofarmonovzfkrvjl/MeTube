from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import User, db, PostVideo
from flask_admin.form.upload import FileUploadField
import os
import cv2

admin = Admin(template_mode="bootstrap3")

class PostVideoView(ModelView):
    form_extra_fields = {
        'video': FileUploadField('video', base_path="videos")
    }

    def extract_90sframe(self, video_path, video_name):
        video_cap = cv2.VideoCapture(video_path)
        frame_number = 90
        video_cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)
        success, frame = video_cap.read()
        if success:
            frame_path = os.path.join("images", f"{video_name}.jpg")
            cv2.imwrite(frame_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        else:
            print("Failed to read video")

    def on_model_change(self, form, model, is_created):
        print(f"Form: {form}\nmodel: {model}\nis_created: {is_created}")
        print(model.video)
        if is_created and model.video:
            video_path = os.path.join("videos", model.video)
            self.extract_90sframe(video_path, model.video)

        return super(PostVideoView, self).on_model_change(form, model, is_created)

    def on_model_delete(self, model):
        print("on model change delete")
        if model.video:
            video_path = f"videos/{model.video}"
            if os.path.exists(video_path):
                os.remove(video_path)
                try:
                    os.remove(f"images/{model.video}.jpg")
                except:
                    pass


admin.add_view(ModelView(User, db.session))
admin.add_view(PostVideoView(PostVideo, db.session))
