// src/VerbFlashcards.tsx

import React, { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight, RotateCcw, CheckCircle, XCircle } from 'lucide-react';

interface Verb {
  base: string;
  past: string;
  participle: string;
}

const VerbFlashcards = () => {
  const verbs = [
    { base: 'be', past: 'was/were', participle: 'been' },
    { base: 'have', past: 'had', participle: 'had' },
    { base: 'do', past: 'did', participle: 'done' },
    { base: 'say', past: 'said', participle: 'said' },
    { base: 'get', past: 'got', participle: 'gotten' },
    { base: 'make', past: 'made', participle: 'made' },
    { base: 'go', past: 'went', participle: 'gone' },
    { base: 'know', past: 'knew', participle: 'known' },
    { base: 'take', past: 'took', participle: 'taken' },
    { base: 'see', past: 'saw', participle: 'seen' },
    { base: 'come', past: 'came', participle: 'come' },
    { base: 'think', past: 'thought', participle: 'thought' },
    { base: 'look', past: 'looked', participle: 'looked' },
    { base: 'want', past: 'wanted', participle: 'wanted' },
    { base: 'give', past: 'gave', participle: 'given' },
    { base: 'use', past: 'used', participle: 'used' },
    { base: 'find', past: 'found', participle: 'found' },
    { base: 'tell', past: 'told', participle: 'told' },
    { base: 'ask', past: 'asked', participle: 'asked' },
    { base: 'work', past: 'worked', participle: 'worked' },
    { base: 'seem', past: 'seemed', participle: 'seemed' },
    { base: 'feel', past: 'felt', participle: 'felt' },
    { base: 'try', past: 'tried', participle: 'tried' },
    { base: 'leave', past: 'left', participle: 'left' },
    { base: 'call', past: 'called', participle: 'called' },
    { base: 'keep', past: 'kept', participle: 'kept' },
    { base: 'let', past: 'let', participle: 'let' },
    { base: 'begin', past: 'began', participle: 'begun' },
    { base: 'help', past: 'helped', participle: 'helped' },
    { base: 'talk', past: 'talked', participle: 'talked' },
    { base: 'turn', past: 'turned', participle: 'turned' },
    { base: 'start', past: 'started', participle: 'started' },
    { base: 'show', past: 'showed', participle: 'shown' },
    { base: 'hear', past: 'heard', participle: 'heard' },
    { base: 'play', past: 'played', participle: 'played' },
    { base: 'run', past: 'ran', participle: 'run' },
    { base: 'move', past: 'moved', participle: 'moved' },
    { base: 'live', past: 'lived', participle: 'lived' },
    { base: 'believe', past: 'believed', participle: 'believed' },
    { base: 'hold', past: 'held', participle: 'held' },
    { base: 'bring', past: 'brought', participle: 'brought' },
    { base: 'happen', past: 'happened', participle: 'happened' },
    { base: 'write', past: 'wrote', participle: 'written' },
    { base: 'provide', past: 'provided', participle: 'provided' },
    { base: 'sit', past: 'sat', participle: 'sat' },
    { base: 'stand', past: 'stood', participle: 'stood' },
    { base: 'lose', past: 'lost', participle: 'lost' },
    { base: 'pay', past: 'paid', participle: 'paid' },
    { base: 'meet', past: 'met', participle: 'met' },
    { base: 'include', past: 'included', participle: 'included' },
    { base: 'continue', past: 'continued', participle: 'continued' },
    { base: 'set', past: 'set', participle: 'set' },
    { base: 'learn', past: 'learned', participle: 'learned' },
    { base: 'change', past: 'changed', participle: 'changed' },
    { base: 'lead', past: 'led', participle: 'led' },
    { base: 'understand', past: 'understood', participle: 'understood' },
    { base: 'watch', past: 'watched', participle: 'watched' },
    { base: 'follow', past: 'followed', participle: 'followed' },
    { base: 'stop', past: 'stopped', participle: 'stopped' },
    { base: 'create', past: 'created', participle: 'created' },
    { base: 'speak', past: 'spoke', participle: 'spoken' },
    { base: 'read', past: 'read', participle: 'read' },
    { base: 'allow', past: 'allowed', participle: 'allowed' },
    { base: 'add', past: 'added', participle: 'added' },
    { base: 'spend', past: 'spent', participle: 'spent' },
    { base: 'grow', past: 'grew', participle: 'grown' },
    { base: 'open', past: 'opened', participle: 'opened' },
    { base: 'walk', past: 'walked', participle: 'walked' },
    { base: 'win', past: 'won', participle: 'won' },
    { base: 'offer', past: 'offered', participle: 'offered' },
    { base: 'remember', past: 'remembered', participle: 'remembered' },
    { base: 'love', past: 'loved', participle: 'loved' },
    { base: 'consider', past: 'considered', participle: 'considered' },
    { base: 'appear', past: 'appeared', participle: 'appeared' },
    { base: 'buy', past: 'bought', participle: 'bought' },
    { base: 'wait', past: 'waited', participle: 'waited' },
    { base: 'serve', past: 'served', participle: 'served' },
    { base: 'die', past: 'died', participle: 'died' },
    { base: 'send', past: 'sent', participle: 'sent' },
    { base: 'expect', past: 'expected', participle: 'expected' },
    { base: 'build', past: 'built', participle: 'built' },
    { base: 'stay', past: 'stayed', participle: 'stayed' },
    { base: 'fall', past: 'fell', participle: 'fallen' },
    { base: 'cut', past: 'cut', participle: 'cut' },
    { base: 'reach', past: 'reached', participle: 'reached' },
    { base: 'kill', past: 'killed', participle: 'killed' },
    { base: 'remain', past: 'remained', participle: 'remained' },
    { base: 'suggest', past: 'suggested', participle: 'suggested' },
    { base: 'raise', past: 'raised', participle: 'raised' },
    { base: 'pass', past: 'passed', participle: 'passed' },
    { base: 'sell', past: 'sold', participle: 'sold' },
    { base: 'require', past: 'required', participle: 'required' },
    { base: 'report', past: 'reported', participle: 'reported' },
    { base: 'decide', past: 'decided', participle: 'decided' },
    { base: 'pull', past: 'pulled', participle: 'pulled' },
    { base: 'break', past: 'broke', participle: 'broken' },
    { base: 'pick', past: 'picked', participle: 'picked' },
    { base: 'wear', past: 'wore', participle: 'worn' },
    { base: 'choose', past: 'chose', participle: 'chosen' },
    { base: 'drive', past: 'drove', participle: 'driven' },
    { base: 'fight', past: 'fought', participle: 'fought' },
    { base: 'catch', past: 'caught', participle: 'caught' },
    { base: 'draw', past: 'drew', participle: 'drawn' },
    { base: 'become', past: 'became', participle: 'become' },
    { base: 'teach', past: 'taught', participle: 'taught' },
    { base: 'eat', past: 'ate', participle: 'eaten' },
    { base: 'fly', past: 'flew', participle: 'flown' }
  ];

  const [currentIndex, setCurrentIndex] = useState(0);
  const [showAnswers, setShowAnswers] = useState(false);
  const [testMode, setTestMode] = useState('base'); // 'base', 'past', 'participle'
  const [userAnswers, setUserAnswers] = useState({ answer1: '', answer2: '' });
  const [feedback, setFeedback] = useState({ show: false, correct: false, message: '' });
  const [shuffledVerbs, setShuffledVerbs] = useState<Verb[]>([]);

  useEffect(() => {
    shuffleVerbs();
  }, []);

  const shuffleVerbs = () => {
    const shuffled = [...verbs].sort(() => Math.random() - 0.5);
    setShuffledVerbs(shuffled);
    setCurrentIndex(0);
    resetCard();
  };

  const resetCard = () => {
    setShowAnswers(false);
    setUserAnswers({ answer1: '', answer2: '' });
    setFeedback({ show: false, correct: false, message: '' });
  };

  const nextCard = () => {
    if (currentIndex < shuffledVerbs.length - 1) {
      setCurrentIndex(currentIndex + 1);
      resetCard();
    }
  };

  const prevCard = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
      resetCard();
    }
  };

  const toggleMode = () => {
    const modes = ['base', 'past', 'participle'];
    const currentModeIndex = modes.indexOf(testMode);
    const nextMode = modes[(currentModeIndex + 1) % modes.length];
    setTestMode(nextMode);
    resetCard();
  };

  const checkAnswers = () => {
    if (!shuffledVerbs.length) return;
    
    const currentVerb = shuffledVerbs[currentIndex];
    let correct1 = false;
    let correct2 = false;
    let expectedAnswers = [];

    if (testMode === 'base') {
      correct1 = userAnswers.answer1.toLowerCase().trim() === currentVerb.past.toLowerCase();
      correct2 = userAnswers.answer2.toLowerCase().trim() === currentVerb.participle.toLowerCase();
      expectedAnswers = [currentVerb.past, currentVerb.participle];
    } else if (testMode === 'past') {
      correct1 = userAnswers.answer1.toLowerCase().trim() === currentVerb.base.toLowerCase();
      correct2 = userAnswers.answer2.toLowerCase().trim() === currentVerb.participle.toLowerCase();
      expectedAnswers = [currentVerb.base, currentVerb.participle];
    } else {
      correct1 = userAnswers.answer1.toLowerCase().trim() === currentVerb.base.toLowerCase();
      correct2 = userAnswers.answer2.toLowerCase().trim() === currentVerb.past.toLowerCase();
      expectedAnswers = [currentVerb.base, currentVerb.past];
    }

    const bothCorrect = correct1 && correct2;
    setFeedback({
      show: true,
      correct: bothCorrect,
      message: bothCorrect 
        ? 'Excellent! Both answers are correct!' 
        : `Correct answers: ${expectedAnswers[0]} / ${expectedAnswers[1]}`
    });
    setShowAnswers(true);
  };

  const getPromptText = () => {
    if (testMode === 'base') {
      return {
        title: 'Base Form Given',
        instruction: 'Provide the past form and past participle:',
        labels: ['Past Form:', 'Past Participle:']
      };
    } else if (testMode === 'past') {
      return {
        title: 'Past Form Given',
        instruction: 'Provide the base form and past participle:',
        labels: ['Base Form:', 'Past Participle:']
      };
    } else {
      return {
        title: 'Past Participle Given',
        instruction: 'Provide the base form and past form:',
        labels: ['Base Form:', 'Past Form:']
      };
    }
  };

  const getCurrentWord = () => {
    if (!shuffledVerbs.length) return '';
    const currentVerb = shuffledVerbs[currentIndex];
    if (testMode === 'base') return currentVerb.base;
    if (testMode === 'past') return currentVerb.past;
    return currentVerb.participle;
  };

  const promptInfo = getPromptText();

  if (!shuffledVerbs.length) return <div>Loading...</div>;

  return (
    <div className="max-w-2xl mx-auto p-6 bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen">
      <div className="bg-white rounded-xl shadow-lg p-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Irregular Verb Flashcards</h1>
          <p className="text-gray-600">Master past forms and past participles</p>
        </div>

        <div className="flex justify-between items-center mb-6">
          <div className="text-sm text-gray-500">
            Card {currentIndex + 1} of {shuffledVerbs.length}
          </div>
          <div className="flex gap-2">
            <button
              onClick={toggleMode}
              className="px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors text-sm"
            >
              Mode: {promptInfo.title}
            </button>
            <button
              onClick={shuffleVerbs}
              className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
          </div>
        </div>

        <div className="bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl p-8 text-white text-center mb-6">
          <div className="text-sm opacity-80 mb-2">{promptInfo.instruction}</div>
          <div className="text-4xl font-bold mb-4">{getCurrentWord()}</div>
        </div>

        <div className="space-y-4 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {promptInfo.labels[0]}
            </label>
            <input
              type="text"
              value={userAnswers.answer1}
              onChange={(e) => setUserAnswers({...userAnswers, answer1: e.target.value})}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              placeholder="Enter your answer..."
              disabled={showAnswers}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {promptInfo.labels[1]}
            </label>
            <input
              type="text"
              value={userAnswers.answer2}
              onChange={(e) => setUserAnswers({...userAnswers, answer2: e.target.value})}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              placeholder="Enter your answer..."
              disabled={showAnswers}
            />
          </div>
        </div>

        {!showAnswers ? (
          <button
            onClick={checkAnswers}
            className="w-full py-3 bg-indigo-500 text-white rounded-lg hover:bg-indigo-600 transition-colors font-medium"
            disabled={!userAnswers.answer1.trim() || !userAnswers.answer2.trim()}
          >
            Check Answers
          </button>
        ) : (
          <div className="space-y-4">
            <div className={`p-4 rounded-lg flex items-center gap-3 ${
              feedback.correct ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
            }`}>
              {feedback.correct ? <CheckCircle className="w-5 h-5" /> : <XCircle className="w-5 h-5" />}
              <span className="font-medium">{feedback.message}</span>
            </div>

            <div className="bg-gray-50 rounded-lg p-4">
              <h3 className="font-semibold text-gray-800 mb-2">Complete Verb Forms:</h3>
              <div className="text-sm text-gray-600">
                <span className="font-medium">Base:</span> {shuffledVerbs[currentIndex].base} • 
                <span className="font-medium"> Past:</span> {shuffledVerbs[currentIndex].past} • 
                <span className="font-medium"> Past Participle:</span> {shuffledVerbs[currentIndex].participle}
              </div>
            </div>
          </div>
        )}

        <div className="flex justify-between items-center mt-8">
          <button
            onClick={prevCard}
            disabled={currentIndex === 0}
            className="flex items-center gap-2 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <ChevronLeft className="w-4 h-4" />
            Previous
          </button>

          <div className="text-sm text-gray-500">
            Progress: {Math.round(((currentIndex + 1) / shuffledVerbs.length) * 100)}%
          </div>

          <button
            onClick={nextCard}
            disabled={currentIndex === shuffledVerbs.length - 1}
            className="flex items-center gap-2 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="mt-6 text-center text-sm text-gray-600">
        <p>💡 Tip: Use the "Mode" button to switch between different testing methods</p>
      </div>
    </div>
  );
};

export default VerbFlashcards;