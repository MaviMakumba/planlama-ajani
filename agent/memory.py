class Memory:
    def __init__(self, max_messages=30):
        self.history = []
        self.max_messages = max_messages

    def add(self, role: str, content: str, tool_calls=None, tool_call_id=None):
        """
        Geçmişe mesaj ekler. 
        - role: 'user', 'assistant' veya 'tool'
        - tool_calls: Assistant bir araç çağırdığında gelen liste
        - tool_call_id: Tool rolündeki mesajlar için zorunlu ID
        """
        message = {"role": role, "content": content}
        
        # Eğer asistan bir araç çağırıyorsa bunu ekle
        if tool_calls:
            message["tool_calls"] = tool_calls
            
        # Eğer bu bir araç cevabıysa ID'yi ekle
        if tool_call_id:
            message["tool_call_id"] = tool_call_id

        self.history.append(message)
        
        # Limit aşılırsa en eski mesajı sil
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