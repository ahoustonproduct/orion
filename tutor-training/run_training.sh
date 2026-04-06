#!/bin/bash

# Make sure we fail fast
set -e

echo "=========================================="
echo " Starting MLX LoRA Fine-Tuning Pipeline   "
echo "=========================================="

echo "[1/4] Ensuring MLX is installed..."
pip install -q mlx-lm

echo "[2/4] Generating training dataset (train.jsonl, valid.jsonl)..."
node generate_dataset.js

# We use the official Gemma 4 E4B architecture.
BASE_MODEL="unsloth/gemma-4-E4B-it"

echo "[3/4] Fine-tuning the base model using MLX LoRA..."
# This executes training. Because it's an 8B/9B model on an M-series mac,
# we use 4-bit precision and relatively small batch sizes.
mlx_lm.lora \
  --model $BASE_MODEL \
  --train \
  --data . \
  --iters 500 \
  --batch-size 2 \
  --learning-rate 1e-5

echo "[4/4] Fusing the LoRA adapter weights directly together..."
# We use --de-quantize to avoid the U32 data type error common in Gemma 4 fusions
mlx_lm.fuse \
  --model $BASE_MODEL \
  --adapter-path adapters \
  --save-path ./orion-fused \
  --de-quantize

echo "Fusing complete. Model saved to ./orion-fused."

echo "Loading into Ollama..."
# Ollama natively supports safetensors importation with a Modelfile
ollama create orion-tutor -f Modelfile

echo "Done! The 'orion-tutor' model is installed to Ollama and ready for inference!"
