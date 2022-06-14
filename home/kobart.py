from transformers import PreTrainedTokenizerFast
from transformers import BartForConditionalGeneration

import torch

class Kobart :
    
    def __init__(self) :
        self.tokenizer = PreTrainedTokenizerFast.from_pretrained('digit82/kobart-summarization')
        self.model     = BartForConditionalGeneration.from_pretrained('digit82/kobart-summarization')
        
    def summary(self, text) :
        ex            = text.replace('\n', ' ')
        raw_input_ids = self.tokenizer.encode(ex)
        input_ids     = [self.tokenizer.bos_token_id] + raw_input_ids + [self.tokenizer.eos_token_id]
        summary_ids   = self.model.generate(torch.tensor([input_ids]),
                                            num_beams    = 4,
                                            max_length   = 512,
                                            eos_token_id = 1)
        return self.tokenizer.decode(summary_ids.squeeze().tolist(), skip_special_tokens = True)
    
    def __str__(self) :
        return 'KoBART'