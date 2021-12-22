
import uuid

class ImageHandler :
    def __init__(self, client, bucket, bucket_url) :
        self.client = client
        self.bucket = bucket
        self.bucket_url = bucket_url

    def upload_file(self, file, directory) :
        file._set_name(str(uuid.uuid4()))
        self.client.Bucket(self.bucket).put_object(
            Key = directory+'/%s'%(file),
            Body = file,
            ContentType = 'jpg'
        )
        return self.bucket_url+"%s/%s"%(directory, file)
    
    def upload_files(self, files, directory) :
        return [self.upload_file(file, directory) for file in files]