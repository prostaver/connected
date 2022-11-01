import os
import sys

from fastapi import UploadFile


ROOT_DIRECTORY = sys.path[0]


async def save_file(uploaded_file: UploadFile = None):
    if not uploaded_file.filename:
        return

    file_loc = ROOT_DIRECTORY + f"/static/images/user_profile/{uploaded_file.filename}"
    with open(file_loc, "wb") as file:
        file.write(await uploaded_file.read())
        uploaded_file.close()