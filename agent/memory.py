class Memory:
    def __init__(self, max_messages=20):
        self.history = []
        self.max_messages = max_messages

    def add(self, role: str, content: str):
        """Geçmişe yeni mesaj ekle. Limit aşılırsa en eskiyi sil."""
        self.history.append({"role": role, "content": content})
        if len(self.history) > self.max_messages:
            self.history = self.history[-self.max_messages:]

    def get_history(self) -> list:
        """Mevcut konuşma geçmişini döndür."""
        return self.history.copy()

    def reset(self):
        """Konuşmayı sıfırla (yeni plan başlatılınca)."""
        self.history = []

    def __len__(self):
        return len(self.history)