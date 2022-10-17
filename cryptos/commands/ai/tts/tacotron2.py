import torch
import torchaudio
from flask import Blueprint

bp = Blueprint('tacotron2', __name__)

@bp.cli.command()
def mix():
  torch.random.manual_seed(0)
  device = "cuda" if torch.cuda.is_available() else "cpu"

  print(torch.__version__)
  print(torchaudio.__version__)
  print(device)
