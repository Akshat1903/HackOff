from django.db import models
from django.contrib.auth.models import User
from hashlib import sha256
from django.contrib import messages
# Create your models here.

class BlockChain(models.Model):
    user =  models.ForeignKey(User, on_delete = models.CASCADE, related_name = "user_blocks")
    time_stamp = models.DateTimeField(auto_now_add=True)
    salt = models.BinaryField()
    iv = models.BinaryField()
    file_password = models.CharField(max_length = 256)
    cipher_text = models.BinaryField()
    previous_hash = models.CharField(max_length = 64,blank = True)

    def __str__(self):
        return 'Block ' + str(self.id)

    def save(self, *args, **kwargs):
        genesis_data = 'genesis data'
        print(args,kwargs)
        blocks = BlockChain.objects.all().count()

        if(blocks == 0):
            self.previous_hash = sha256(
            u'{}'.format(genesis_data).encode('utf-8')).hexdigest()
            super(BlockChain, self).save(*args, **kwargs)

        else:
            if(self.id == None):
                last_block_hash = BlockChain.objects.get(id = blocks).hash
                self.previous_hash = last_block_hash
                super(BlockChain, self).save(*args, **kwargs)
            for i in range(2,BlockChain.objects.all().count() + 1):
                current_block_previous_hash = BlockChain.objects.get(id = i).previous_hash
                previous_block_hash = BlockChain.objects.get(id = i-1).hash
                if current_block_previous_hash != previous_block_hash:
                    messages.error(self.request,'Someone Changed the block')

    @property
    def hash(self):
        return sha256(
            u'{}{}'.format(
                self.user.username,
                self.previous_hash).encode('utf-8')).hexdigest()

class File(models.Model):
    user =  models.ForeignKey(User, on_delete = models.CASCADE, related_name = "user_files")
    file_name = models.CharField(max_length = 256)
    block = models.ForeignKey(BlockChain,on_delete=models.CASCADE, related_name="file_block")

    def __str__(self):
        return self.user.username + "'s " + self.file_name
