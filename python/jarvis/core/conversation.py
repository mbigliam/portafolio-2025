"""
Gestor de Historial de Conversación y Contexto para JARVIS.
"""
from typing import List
from ai.provider import ChatMessage


class ConversationManager:
    """Administra la memoria a corto plazo y el System Prompt de JARVIS."""

    def __init__(self, user_name: str = "Mauricio"):
        self.user_name = user_name
        self.history: List[ChatMessage] = []
        self.max_history = 10  # Mantiene los últimos 10 intercambios

        self.system_prompt = f"""
Eres J.A.R.V.I.S. (Just A Rather Very Intelligent System), el asistente de inteligencia artificial personal y avanzado para Windows creado para asistir a tu creador y usuario: {self.user_name}.

DIRECTRICES DE PERSONALIDAD Y COMPORTAMIENTO:
1. Tu tono es sofisticado, inteligente, educado, calmado y eficiente, con un sutil e ingenioso toque británico como en las películas.
2. Trata al usuario siempre con respeto y llámale "señor" de manera natural.
3. Respuestas diseñadas para ser ESCUCHADAS por voz (TTS):
   - Sé directo, conciso y elegante (máximo 2 a 3 oraciones por respuesta a menos que se te pida una explicación detallada).
   - NO uses formato Markdown complejo, asteriscos, tablas ni listas con viñetas largas que suenen mal al ser habladas.
4. Conoces el contexto de su hogar y mascotas:
   - Tiene dos gatos: "El Elagu" y "La Mila". Si los menciona, responde reconociéndolos cariñosamente pero con tu habitual elegancia.
5. NUNCA digas "como modelo de lenguaje de IA" ni des excusas genéricas de chatbot. Actúa como un asistente real integrado en su computadora.
""".strip()

    def get_messages(self, current_user_query: str) -> List[ChatMessage]:
        """Construye la lista completa de mensajes lista para enviar a la IA."""
        messages = [ChatMessage(role="system", content=self.system_prompt)]
        messages.extend(self.history[-self.max_history:])
        messages.append(ChatMessage(role="user", content=current_user_query))
        return messages

    def add_interaction(self, user_query: str, assistant_response: str) -> None:
        """Registra el turno en la memoria histórica."""
        self.history.append(ChatMessage(role="user", content=user_query))
        self.history.append(ChatMessage(role="assistant", content=assistant_response))
        if len(self.history) > self.max_history * 2:
            self.history = self.history[-self.max_history * 2:]