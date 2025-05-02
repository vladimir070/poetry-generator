import nltk
import random
from collections import defaultdict
from nltk.corpus import cmudict, words

nltk.download('cmudict', quiet=True)
nltk.download('words', quiet=True)

# ========== Конфигурация ==========
THEMES = {
    'nature': {
        'nouns': ['moon', 'star', 'wind', 'ocean', 'mountain', 'forest', 'river', 'stone', 'tree', 'sky'],
        'verbs': ['whispers', 'dances', 'flows', 'awakens', 'illuminates', 'carves', 'echoes', 'sings', 'rises', 'breathes'],
        'adjectives': ['ancient', 'silent', 'radiant', 'crimson', 'eternal', 'hollow', 'luminous', 'majestic', 'gentle', 'timeless'],
        'syllables': {
            'moon':1, 'star':1, 'wind':1, 'ocean':2, 'mountain':2,
            'forest':2, 'river':2, 'stone':1, 'tree':1, 'sky':1
        }
    }
}

POETRY_CORPUS = [
    "the silent moon whispers to the sea",
    "crimson shadows dance with memories old",
    "ancient winds carry tales untold",
    "in the forest of time stories unfold",
    "dawn's first light breaks the night",
    "stones remember what hands have molded",
    "rivers sing songs of the earth's heartbeat",
    "mountains wear crowns of celestial heat",
    "ocean depths guard secrets complete",
    "stars write fate in lines discrete",
    "where shadows weave through ancient trees",
    "the ocean's breath sings melodies",
    "mountains rise where earth meets sky",
    "in twilight's glow the fireflies die",
    "a stone remembers every tear",
    "the wind composes songs we hear",
    "moonlight paints the silver trail",
    "whispers of dawn make night grow pale",
    "where shadows melt in morning's glow",
    "the river's song ebbs soft and low",
    "beneath the bark, old secrets sleep",
    "the nightingale's lament runs deep",
    "frost etches tales on windowpanes",
    "the comet trails celestial chains"
]


FALLBACK_LINES = [
    "Moonlight weaves through silvered leaves",
    "Horizons breathe with ancient sighs",
    "Tides of time erode the shore",
    "The void between the stars implores",
    "Whispers dance through moonlit air",
    "Eternal stars ignite despair",
    "Rivers flow with timeless grace",
    "Night unveils its hidden face"
]

# ========== Цепь Маркова ==========
class MarkovGenerator:
    def __init__(self):
        self.chain = defaultdict(list)
        self.build_chain()
    
    def build_chain(self):
        for line in POETRY_CORPUS:
            words = line.lower().split()
            for i in range(len(words)-1):
                self.chain[words[i]].append(words[i+1])
    
    def generate_line(self, seed_word, length=6):
        line = [seed_word.capitalize()]
        current_word = seed_word.lower()
        for _ in range(length-1):
            next_words = self.chain.get(current_word, [])
            if not next_words:
                next_words = list(self.chain.keys())
            current_word = random.choice(next_words)
            line.append(current_word)
        return ' '.join(line)

# ========== Система рифмовки ==========
class RhymeEngine:
    def __init__(self):
        self.cmudict = cmudict.dict()
        self.word_list = set(words.words())
        self.fallback_rhymes = {
            'ight': ['light', 'night', 'bright', 'sight', 'flight'],
            'oon': ['moon', 'tune', 'dune', 'spoon', 'lagoon']
        }
    
    def get_rhymes(self, word):
        word = word.lower()
        rhymes = set()
        
        if word in self.cmudict:
            for pron in self.cmudict[word]:
                for w, prons in self.cmudict.items():
                    if w == word: continue
                    if any(p[-2:] == pron[-2:] for p in prons):
                        if w in self.word_list:
                            rhymes.add(w)
        
        if not rhymes:
            for ending, group in self.fallback_rhymes.items():
                if word.endswith(ending):
                    return group
        
        return list(rhymes)[:3]

# ========== Основной генератор ==========
class PoetryGenerator:
    def __init__(self, theme='nature'):
        self.theme = theme
        self.markov = MarkovGenerator()
        self.rhyme_engine = RhymeEngine()
        self.used_words = set()
        self.syllable_target = 8
    
    def _get_valid_word(self, category):
        if random.random() < 0.3:  # 30% chance для нового seed
            self.used_words.clear()
            
        theme_words = THEMES[self.theme][category]
        available = [w for w in theme_words if w not in self.used_words]
        return random.choice(available) if available else random.choice(theme_words)
    
    def _count_syllables(self, word):
        return THEMES[self.theme]['syllables'].get(word, 1)
    
    def generate_poem(self, scheme='ABAB'):
        lines = []
        rhyme_pairs = []
        
        for line_num in range(4):
            for attempt in range(50):
                seed = self._get_valid_word('nouns')
                line = self.markov.generate_line(seed)
                
                if 'syllables' in THEMES[self.theme]:
                    syllables = sum(self._count_syllables(word) for word in line.split() 
                                  if word in THEMES[self.theme]['syllables'])
                    if abs(syllables - self.syllable_target) > 3:
                        continue
                
                if all(word in (THEMES[self.theme]['nouns'] + 
                                THEMES[self.theme]['verbs'] + 
                                THEMES[self.theme]['adjectives'])
                      for word in line.lower().split()):
                    break
            else:
                line = random.choice(FALLBACK_LINES)
            
            rhyme_word = line.split()[-1].rstrip('.,!?')
            rhymes = self.rhyme_engine.get_rhymes(rhyme_word)
            
            if scheme == 'ABAB':
                if line_num % 2 == 0:
                    rhyme_pairs.append(rhyme_word)
                else:
                    if rhymes and rhyme_pairs:
                        rhyme_word = random.choice(rhymes)
            
            lines.append(line.capitalize() + '.')
            self.used_words.update(set(line.lower().split()))
        
        return '\n'.join(lines)

# ========== Использование ==========
if __name__ == "__main__":
    generator = PoetryGenerator(theme='nature')
    print("Generated Poem:\n")
    print(generator.generate_poem())