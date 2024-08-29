import json
from typing import List
from fastapi import FastAPI, HTTPException, status
from models import SnowBoard

app = FastAPI()

file_path = "snowboards.json"

def load_snowboards() -> List[SnowBoard]:
    """Load snowboards from the JSON file."""
    try:
        with open(file_path, "r") as f:
            snowboard_list = json.load(f)
        return [SnowBoard(**board) for board in snowboard_list]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error reading the data file")

def save_snowboards(snowboards: List[SnowBoard]) -> None:
    """Save snowboards to the JSON file."""
    try:
        with open(file_path, "w") as f:
            json.dump([board.model_dump() for board in snowboards], f, indent=4)
    except IOError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error writing to the data file")

boards: List[SnowBoard] = load_snowboards()

@app.get("/snowboards")
async def list_boards() -> List[SnowBoard]:
    return boards

@app.post("/snowboards")
async def add_board(snowboard: SnowBoard) -> dict:
    # Check if the ID is already used
    if any(board.id == snowboard.id for board in boards):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID already exists")

    boards.append(snowboard)
    save_snowboards(boards)
    return {"message": "Snowboard added successfully"}

@app.put("/snowboards/{id}")
async def update_snowboard(id: int, updated_snowboard: SnowBoard) -> dict:
    for i, board in enumerate(boards):
        if board.id == id:
            updated_snowboard.id = id  # Ensure ID is preserved
            boards[i] = updated_snowboard
            save_snowboards(boards)
            return {"message": "Snowboard updated successfully"}
    
    # If not found, add as new snowboard
    updated_snowboard.id = id
    boards.append(updated_snowboard)
    save_snowboards(boards)
    return {"message": "Snowboard added successfully"}

@app.delete("/snowboards/{id}")
async def delete_snowboard(id: int) -> dict:
    for i, board in enumerate(boards):
        if board.id == id:
            del boards[i]
            save_snowboards(boards)
            return {"message": "Snowboard deleted successfully"}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Snowboard not found")
