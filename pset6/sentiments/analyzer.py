import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        
        self.positives = []
        self.negatives = []
        
        with open(positives) as positive:
            for line in positive:
                if not line.startswith((" ", ";")):
                    self.positives.extend(line.split())
                    
        with open(negatives) as negative:
            for line in negative:
                if not line.startswith((" ", ";")):
                    self.negatives.extend(line.split())    
     

    def analyze(self, text): 
        """Analyze text for sentiment, returning its score."""

        
        tokenizer = nltk.tokenize.TweetTokenizer()
        tokens = tokenizer.tokenize(text)
        score = 0
        for token in tokens:
            token.lower()
            
            if token in self.positives:
                score =+ 1
            elif token in self.negatives:
                score =- 1
                
        return score
