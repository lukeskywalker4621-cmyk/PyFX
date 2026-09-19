from PySide6.QtWidgets import QFileDialog

def import_files(parent=None):
    files, _ = QFileDialog.getOpenFileNames(
        parent,
        "Import Files",
        "",
        "Media Files (*.mp4 *.mov *.avi *.mkv *.png *.jpg *.wav *.mp3);;"
    )

    return files