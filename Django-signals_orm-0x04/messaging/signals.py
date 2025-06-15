from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            old = Message.objects.get(pk=instance.pk)
            if old.content != instance.content:
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old.content,
                    edited_by=instance.sender  # You can adjust this logic if sender is not the editor
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass
