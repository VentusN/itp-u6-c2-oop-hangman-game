from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self,char,miss=None,hit=None):
        if miss and hit:                        
            raise InvalidGuessAttempt()
        self.char = char.lower()
        self.miss = miss
        self.hit = hit
        
    def is_hit(self):
        return bool(self.hit)                  
    
    def is_miss(self):
        return bool(self.miss)
    

class GuessWord(object):
    
    def __init__(self,answer):
        if not answer:                         
            raise InvalidWordException()
        self.answer = answer.lower()           
        self.masked = "".join('*' for char in self.answer) 
    
    def perform_attempt(self,character):
        if len(character) > 1:                 
            raise InvalidGuessedLetterException()
            
        self.character = character.lower()     
        
        if self.character not in self.answer:
            return GuessAttempt(self.character, miss=True)  
        
        new_mword=''
        for answer_char, masked_char in zip(self.answer, self.masked):
            if answer_char == self.character:
                new_mword += answer_char
            else:
                new_mword += masked_char
        
        self.masked = new_mword
        return GuessAttempt(self.character, hit=True)

class HangmanGame(object):
    
    WORD_LIST=['rmotr', 'python', 'awesome']
    
    def __init__(self, word_list=None, number_of_guesses=5):
        if not word_list:
            word_list = self.WORD_LIST
        self.previous_guesses = []
        self.remaining_misses = number_of_guesses
        self.word = GuessWord(self.select_random_word(word_list))
    
    @classmethod
    def select_random_word(cls,word_list):
        if not word_list:
            raise InvalidListOfWordsException()
        return random.choice(word_list)
    
    
    def guess(self,letter):
        self.letter = letter.lower()
        
        if self.letter in self.previous_guesses:
            raise InvalidGuessedLetterException()
        
        if self.is_finished():
            raise GameFinishedException()
            
        self.previous_guesses.append(self.letter)
        
        attempt = self.word.perform_attempt(self.letter)
        
        if attempt.is_miss():
            self.remaining_misses -=1
        
        if self.is_won():
            raise GameWonException()
        
        if self.is_lost():
            raise GameLostException()
            
        return attempt

    
    def is_won(self):
        return self.word.masked == self.word.answer
        
    def is_lost(self):
        return self.remaining_misses == 0
    
    def is_finished(self):
        return self.is_lost() or self.is_won()
        
