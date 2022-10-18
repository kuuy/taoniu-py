# import torch
# import torchaudio
from flask import Blueprint

bp = Blueprint('tacotron2', __name__)

@bp.cli.command()
def mix():
  # torch.random.manual_seed(0)
  # device = "cuda" if torch.cuda.is_available() else "cpu"
  #
  # bundle = torchaudio.pipelines.TACOTRON2_WAVERNN_PHONE_LJSPEECH
  # processor = bundle.get_text_processor()
  # tacotron2 = bundle.get_tacotron2().to(device)
  # vocoder = bundle.get_vocoder().to(device)
  #
  # text = "who register for a Binance account"
  #
  # with torch.inference_mode():
  #   processed, lengths = processor(text)
  #   processed = processed.to(device)
  #   lengths = lengths.to(device)
  #   spec, spec_lengths, _ = tacotron2.infer(processed, lengths)
  #   waveforms, lengths = vocoder(spec, spec_lengths)
  #
  # torchaudio.save("output_wavernn.wav", waveforms[0:1].cpu(), sample_rate=vocoder.sample_rate)
  pass
