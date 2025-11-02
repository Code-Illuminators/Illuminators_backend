from django.db import models

class Vote(models.Model):
    """Class for storing votes"""
    ROLE_ACCESS = [
        ('simple', 'Simple'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('architect', 'Architect'),
        ('inquisition', 'Inquisition')
    ]
    VOTE_TYPE = [
        ('promotion', 'Promotion'),
        ('excommunication', 'Excommunication'),
    ]
    nominated_user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='nominated_votes')
    vote_type = models.CharField(max_length=20, choices=VOTE_TYPE)
    roles_allowed_vote = models.JSONField(default=list)
    promotion_role = models.CharField(max_length=20, choices=ROLE_ACCESS, null=True, blank=True)
    for_amount = models.IntegerField(default=0)
    against_amount = models.IntegerField(default=0)
    progress = models.FloatField(default=0.0)
    def __str__(self):
        """Return a string representation of the Vote model"""
        return f"Vote for {self.nominated_user.username} — For: {self.for_amount}, Against: {self.against_amount}"
    
    def update_progress(self):
        """Uptade voting progress"""
        total=self.vote_logs.count()
        voted=self.vote_logs.filter(status=True).count()
        if total > 0:
            self.progress=(voted/total*100)
            self.save(update_fields=['progress'])

class VoteLog(models.Model):
    """Class for storing vote logs"""
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, related_name='vote_logs')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='vote_logs')
    is_for = models.BooleanField(default=False)
    is_against = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    def __str__(self):
        """Return a string representation of the VoteLog model"""
        return f"VoteLog for {self.user.username} on vote {self.vote.id}"
