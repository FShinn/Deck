"""This is the deck module.

This module defines the Deck class,
which is similar to a list class which
offers randomized methods.
"""

__all__ = ["Deck"]
__version__ = "1.0"
__author__ = "Sam Shinn"

from math import log
import random

class Deck:
    """This is class simulates a structure like a deck of cards.
    
    This class heavily uses Python's stack-like features of list operations
    to simulate the behavior of a deck of cards. 
    """
    
    # ————————————— magic functions ————————————— 
    def __init__(self, cards=[]):
        if isinstance(cards,Deck):
            self.cards = cards.cards.copy
        else:
            self.cards = list(cards)
    
    def __repr__(self):
        return repr(self.cards)
    
    def __str__(self):
        return str(self.cards)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        """Iterating over Deck removes all cards from Deck"""
        card = self.draw()
        if card is not None:
            return card
        else: 
            raise StopIteration
    
    def __len__(self):
        return len(self.cards)
    
    def __contains__(self, x):
        return x in self.cards
    
    def __nonzero__(self):
        return self.cards.__nonzero__()
    
    # ————————————— primary functions ————————————— 
    def draw(self):
        """Pulls top card from Deck, if any"""
        if self.cards:
            return self.cards.pop()
    
    def place(self, card):
        """Places a card on the top of the Deck"""
        self.cards.append(card)
    
    def search(self, card):
        """Finds, removes, and returns the specified card"""
        if card in self:
            return self.cards.pop(self.cards.index(card))
    
    def flip(self):
        """Flips the deck upside down"""
        self.cards = [card for card in self]
        return self
    
    def split(self, index):
        """Cuts the Deck into two portions.
        
        The return value of this function is a tuple containing two Decks.
        The two Decks are non-overlaping and exhaustive top and bottom
        portions of the original Deck.
        """
        return (Deck(self.cards[index:]), Deck(self.cards[:index]))
    
    def combine(self, otherDeck):
        """Adds the contents of another Deck to this Deck."""
        self.cards += otherDeck.cards
        return self
    
    # ————————————— secondary functions ————————————— 
    def cut(self):
        """Cuts the Deck into two portions.
        
        The return value of this function is a tuple containing two Decks.
        To split the Deck, a normal probability curve is used to introduce
        some randomness to midpoint selection.
        """
        if len(self) < 2:
            raise ValueError("cannot cut deck of less than 2 cards")
        mean = len(self.cards)/2
        if len(self) >= 8:
            standarddeviation = log(len(self))-2
        else:
            standarddeviation = 0
        cutindex = -1
        while cutindex <= 0 or cutindex >= len(self.cards):
            cutindex = int(random.gauss(mean, standarddeviation)+0.5)
        return self.split(cutindex)
    
    def shuffle(self, kind='riffle', aux=None):
        """Shuffles the deck according to some kind of shuffle style
        
        aux paramater is only used on certain shuffle types.
        """
        kind = kind.lower()
        if 'overhand'.startswith(kind):
            self._overhand()
        elif 'riffle'.startswith(kind):
            self._riffle(aux)
        elif 'fisheryates'.startswith(kind):
            self._fisheryates()
        else:
            raise NameError(kind)
        return self
    
    # ————————————— shuffle variants ————————————— 
    def _overhand(self):
        """Shuffles the Deck in the overhand style
        
        This style breaks the Deck into chunks and reverses their order.
        The size of these chunks is determined by normal probability curve.
        """
        newdeck = []
        while self:
            chunksize = int(random.gauss(len(self)/4, len(self)/16))+1
            newdeck += self.cards[len(self)-chunksize:]
            self.cards = self.cards[:len(self)-chunksize]
        self.cards = newdeck
        return self

    def _riffle(self, probability):
        """Shuffles the Deck in the riffle style
        
        This style splits the Deck into two halves and then interleaves them.
        
        Probability changes how 'good' at interleaving the function is.
        
        Some deck fiddlyness occurs during initialization.
        When interleaving decks, we are drawing from the bottom of each deck
        to build our new deck. Thus the top and bottom portions are flipped.
        Also, the top and bottom card of the new deck should be forced new.
        The future topcard is saved for placement later and the bottommost 
        card is placed explicitly before the main interleaving process.
        """
        if not probability:
            probability = [(len(self)-1)/len(self),1/len(self)]
        top, bottom = self.cut()
        self.cards.clear()
        # aforementioned 'deck fiddlyness'
        topcard = bottom.draw()
        top.flip()
        bottom.flip()
        self.place(top.draw())
        last = top
        while top and bottom:
            if random.choices([True,False],weights=probability)[0]:
                if last == top:
                    self.place(bottom.draw())
                    last = bottom
                else:
                    self.place(top.draw())
                    last = top
            else:
                self.place(last.draw())
        self.combine(top.flip())
        self.combine(bottom.flip())
        self.place(topcard)
        return self
    
    def _fisheryates(self):
        """Shuffles the Deck in a Fisher-Yates style.
        
        This style is to use a random permutation of cards where the 
        probabilities of any permutation is randomly distributed.
        Python's random module offers an implementation of this shuffle style.
        """
        random.shuffle(self.cards)
        return self
    
    
