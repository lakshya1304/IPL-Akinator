from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import random
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from engine.bayesian_engine import initialize, update_probabilities
from engine.entropy_selector import select_best_question
from engine.question_templates import QUESTION_MAP
from engine.feedback_learner import save_failure
from engine.session_memory import SessionMemory
from engine.question_generator import generate_dynamic_question
from engine.advanced_reasoner import generate_contextual_reasoning

app = FastAPI()

# ===== CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== GET BASE PATH =====
BASE_DIR = Path(__file__).resolve().parent
DATABASE_DIR = BASE_DIR / "database"

# ===== LOAD DATA =====
players_path = DATABASE_DIR / "players.json"
profiles_path = DATABASE_DIR / "player_profiles.json"

if not players_path.exists():
    raise FileNotFoundError(f"Players database not found at {players_path}")
if not profiles_path.exists():
    raise FileNotFoundError(f"Player profiles database not found at {profiles_path}")

with open(players_path, "r", encoding="utf-8") as f:
    players = json.load(f)

with open(profiles_path, "r", encoding="utf-8") as f:
    player_profiles = json.load(f)

# ===== STATE =====
game_state = {}
memory = SessionMemory()

# ===== HOME =====
@app.get("/")
def home():
    return {"message": "🏏 IPL AI ENGINE ACTIVE"}

# ===== START =====
@app.get("/start")
def start_game():
    global game_state, memory

    memory = SessionMemory()

    probs = initialize(players)

    asked_features = []
    asked_questions = []

    first_feature = select_best_question(players, probs, [])

    first_question = QUESTION_MAP.get(
        first_feature,
        f"Does your player have {first_feature}?"
    )

    asked_features.append(first_feature)
    asked_questions.append(first_question)

    game_state = {
        "probs": probs,
        "asked_features": asked_features,
        "asked_questions": asked_questions,
        "current_feature": first_feature,
        "current_question": first_question,
        "step": 1,
        "history": [],
        "last_guess": None
    }

    return {
        "question": first_question,
        "step": 1,
        "confidence": 0,
        "remaining_candidates": len(players),
        "top_candidates": []
    }

# ===== ANSWER =====
@app.post("/answer")
def answer(ans: str):

    global game_state, memory

    probs = game_state["probs"]
    current_feature = game_state["current_feature"]
    current_question = game_state["current_question"]
    asked_features = game_state["asked_features"]
    asked_questions = game_state["asked_questions"]
    history = game_state["history"]
    step = game_state["step"]

    # ===== MEMORY =====
    memory.add(current_question, ans)

    history.append({
        "question": current_question,
        "answer": ans
    })

    # ===== UPDATE =====
    probs = update_probabilities(players, probs, current_feature, ans)

    # ===== SORT =====
    sorted_players = sorted(probs.items(), key=lambda x: x[1], reverse=True)

    top_player = sorted_players[0][0]
    top_prob = sorted_players[0][1]
    second_prob = sorted_players[1][1] if len(sorted_players) > 1 else 0.001

    # ===== CONFIDENCE =====
    confidence = round((top_prob / (top_prob + second_prob)) * 100, 2)

    # ===== REMAINING =====
    remaining_candidates = len([p for p in probs if probs[p] > 0.01])

    # ===== TOP CANDIDATES =====
    top_candidates = [
        {"name": p, "probability": round(prob * 100, 2)}
        for p, prob in sorted_players[:5]
    ]

    # ===== REASONING =====
    reasoning = generate_contextual_reasoning(
        memory.get_context(),
        top_candidates
    ) + " | Hybrid AI + probabilistic reasoning"

    # ===== UPDATE STATE =====
    game_state["probs"] = probs
    game_state["history"] = history
    game_state["last_guess"] = top_player

    # ===== FINAL =====
    if confidence >= 80 or step >= 8:
        profile = player_profiles.get(top_player, {})
        return {
            "final": True,
            "player": top_player,
            "confidence": confidence,
            "reasoning": reasoning,
            "remaining_candidates": remaining_candidates,
            "top_candidates": top_candidates,
            "step": step,
            "profile": profile
        }

    # ===== NEXT FEATURE =====
    next_feature = select_best_question(players, probs, asked_features)

    # ===== HYBRID QUESTION (SMART RANDOM) =====
    if random.random() < 0.6:
        # AI question
        ai_question = generate_dynamic_question(
            memory.get_context(),
            top_candidates,
            asked_questions
        )
    else:
        # logic question
        ai_question = QUESTION_MAP.get(
            next_feature,
            f"Does your player have {next_feature}?"
        )

    # ===== FAILSAFE =====
    if ai_question in asked_questions or len(ai_question) < 5:
        ai_question = QUESTION_MAP.get(
            next_feature,
            f"Does your player have {next_feature}?"
        )

    # ===== UPDATE TRACKING =====
    asked_features.append(next_feature)
    asked_questions.append(ai_question)

    game_state["current_feature"] = next_feature
    game_state["current_question"] = ai_question
    game_state["asked_features"] = asked_features
    game_state["asked_questions"] = asked_questions
    game_state["step"] += 1

    return {
        "final": False,
        "question": ai_question,
        "guess": top_player,
        "confidence": confidence,
        "reasoning": reasoning,
        "remaining_candidates": remaining_candidates,
        "top_candidates": top_candidates,
        "step": step + 1
    }

# ===== FEEDBACK =====
@app.post("/feedback")
def feedback(correct_player: str):

    global game_state

    save_failure(
        game_state.get("history", []),
        game_state.get("last_guess", "Unknown"),
        correct_player
    )

    return {"message": "AI learning updated"}