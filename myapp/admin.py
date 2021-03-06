from django.contrib import admin
from .models import TransWalk, TransIndiv



class Trans_Walk(admin.ModelAdmin):
    list_display = ('ASRid', 'Audio_File_Link', 'Transcripted_Text', 'caller_phone_number',  'ASR_text', 'audio_duration', 'IsOpenFlag', 'Updated_At', 'click_timestamp', 'Trans_Counter', 'Transcribers_Checked')
    ordering = ['-Updated_At']
    list_filter = ('Updated_At', 'Trans_Counter', 'IsOpenFlag', 'caller_phone_number')
    search_fields = ['ASRid', 'caller_phone_number']
    list_per_page = 8
admin.site.register(TransWalk, Trans_Walk)

class Trans_Indiv(admin.ModelAdmin):
    list_display = ('id', 'asrid', 'audio_file_link', 'audio_duration', 'Text_Indiv', 'Transcribed_At', 'counter_left', 'Transcribed_By')
    ordering = ['-Transcribed_At']
    list_filter = ('audio_duration', 'Transcribed_At', 'counter_left', 'Transcribed_By')
    list_per_page = 8
admin.site.register(TransIndiv, Trans_Indiv)
