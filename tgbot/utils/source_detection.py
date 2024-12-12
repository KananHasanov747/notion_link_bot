from aiogram import types


async def detect_forward_source(message: types.Message) -> str | None:
    """
    Detect the source of the forwarded message.
    """
    if message.forward_from:
        user = message.forward_from
        return (
            f"User: {user.full_name} | ID:{user.username if user.username else 'N/A'}"
        )
    elif message.forward_from_chat:
        chat = message.forward_from_chat
        return f"Chat: {chat.title} | ID:{chat.username if chat.username else 'N/A'}"
    elif message.forward_sender_name:
        return f"Anonymous: {message.forward_sender_name}"
    else:
        return None
