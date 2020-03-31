from datetime import datetime
from django.db import models


class Audio_Info(models.Model):
    wav_file_links = models.CharField(max_length=200, help_text='Audio Links')
    Auto_Transcribed_Text = models.TextField(help_text='Auto Transcribed Text From The ASR')
    created_at = models.DateTimeField(auto_now_add=True)

#    def __str__(self):
#            """String for representing the Model object."""
#            return self.wav_file_links


class TransWalk(models.Model):
    ASRid = models.AutoField(primary_key=True)
    Audio_File_Link = models.CharField(max_length=200, help_text='Audio Links')
    audio_duration = models.DurationField(blank=True, null=True)
    ASR_text = models.TextField(help_text='ASR Output', null=True, blank=True)
    Transcripted_Text = models.TextField(help_text='Most Recent Transcripted Text')
    IsOpenFlag = models.BooleanField(default=False, null=True, blank=True)
    Updated_At = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Trans_Counter = models.IntegerField(default=0, null=True, blank=True)
    Transcribers_Checked = models.CharField(max_length=200, help_text='Usernames of the transcribers Who checked the specific audio', null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return str(self.ASRid)

class TransIndiv(models.Model):
    asrid = models.ForeignKey(TransWalk, on_delete=models.CASCADE)
    audio_file_link = models.CharField(max_length=200, help_text='Audio Links')
    Text_Indiv = models.TextField()
    audio_duration = models.DurationField(blank=True, null=True)
    counter_left = models.IntegerField(null=True)
    Transcribed_At = models.DateTimeField(auto_now_add=True)
    Transcribed_By = models.CharField(max_length=50)
    
