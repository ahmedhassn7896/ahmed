import random
import uuid
from datetime import datetime
from faker import Faker

fake = Faker()

def generate_transaction():
    """Generates a mock e-commerce transaction."""
    return {
        "transaction_id": str(uuid.uuid4()),
        "user_id": str(random.randint(1000, 9999)),
        "product_id": f"PROD-{random.randint(100, 500)}",
        "amount": round(random.uniform(5.0, 500.0), 2),
        "status": random.choice(["success", "success", "success", "failed", "pending"]),
        "transaction_time": datetime.utcnow().isoformat()
    }
