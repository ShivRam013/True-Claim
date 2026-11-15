test_cases = [
    {
        "claim": "LoRA reduces the number of trainable parameters compared with full fine-tuning.",
        "ground_truth": "Supported. LoRA reduces trainable parameters by introducing low-rank trainable matrices while keeping the original model weights frozen."
    },
    {
        "claim": "Increasing the number of trainable parameters always improves model performance.",
        "ground_truth": "Insufficient. Increasing trainable parameters does not guarantee better performance in every task or setting."
    },
    {
        "claim": "Every machine learning model performs equally well on every dataset.",
        "ground_truth": "Contradicted. Model performance varies depending on the dataset, task, data distribution, and model architecture."
    }
]