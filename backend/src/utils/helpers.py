import aiofiles

async def save_upload_file(upload_file, destination):
    async with aiofiles.open(destination, 'wb') as out_file:
        content = await upload_file.read()
        await out_file.write(content)
