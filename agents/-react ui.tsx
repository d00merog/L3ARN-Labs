// App.js
import React from 'react';
import { ThemeProvider } from "@/components/theme-provider";
import MultiSubjectTeacher from './components/MultiSubjectTeacher';

const App = () => (
  <ThemeProvider defaultTheme="light" storageKey="vite-ui-theme">
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Multi-Subject Teacher AI</h1>
      <MultiSubjectTeacher />
    </div>
  </ThemeProvider>
);

export default App;

// components/MultiSubjectTeacher.js
import React, { useState } from 'react';
import SubjectSelector from './SubjectSelector';
import TopicSelector from './TopicSelector';
import LessonDisplay from './LessonDisplay';
import ExerciseModal from './ExerciseModal';
import FeedbackDisplay from './FeedbackDisplay';
import { Button } from "@/components/ui/button";
import { BookOpen } from 'lucide-react';
import { useLesson } from '../hooks/useLesson';

const MultiSubjectTeacher = () => {
  const [subject, setSubject] = useState('');
  const [topic, setTopic] = useState('');
  const [showExercise, setShowExercise] = useState(false);
  const { lesson, feedback, discussion, fetchLesson, checkAnswer } = useLesson();

  const handleGetLesson = () => {
    fetchLesson(subject, topic);
  };

  return (
    <div>
      <SubjectSelector onSelect={setSubject} />
      {subject && <TopicSelector subject={subject} onSelect={setTopic} />}
      <Button onClick={handleGetLesson} disabled={!subject || !topic} className="mb-4">
        Get Lesson
      </Button>
      {lesson && (
        <>
          <LessonDisplay lesson={lesson} subject={subject} topic={topic} />
          <Button onClick={() => setShowExercise(true)} className="mb-4">
            <BookOpen className="mr-2 h-4 w-4" /> Practice Exercise
          </Button>
        </>
      )}
      <ExerciseModal 
        isOpen={showExercise} 
        onClose={() => setShowExercise(false)}
        exercise={lesson?.exercise}
        onSubmit={checkAnswer}
      />
      <FeedbackDisplay feedback={feedback} discussion={discussion} />
    </div>
  );
};

export default MultiSubjectTeacher;

// components/SubjectSelector.js
import React from 'react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

const subjects = ["Math", "Science", "Language", "History"];

const SubjectSelector = ({ onSelect }) => (
  <Select onValueChange={onSelect}>
    <SelectTrigger className="w-full mb-4">
      <SelectValue placeholder="Select a subject" />
    </SelectTrigger>
    <SelectContent>
      {subjects.map((subject) => (
        <SelectItem key={subject} value={subject}>{subject}</SelectItem>
      ))}
    </SelectContent>
  </Select>
);

export default SubjectSelector;

// components/TopicSelector.js
import React from 'react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

const topicsBySubject = {
  Math: ["Algebra", "Geometry", "Calculus", "Statistics"],
  Science: ["Biology", "Chemistry", "Physics", "Earth Science"],
  Language: ["Grammar", "Vocabulary", "Conversation", "Translation"],
  History: ["Ancient Civilizations", "Middle Ages", "Renaissance", "Modern Era"]
};

const TopicSelector = ({ subject, onSelect }) => (
  <Select onValueChange={onSelect}>
    <SelectTrigger className="w-full mb-4">
      <SelectValue placeholder="Select a topic" />
    </SelectTrigger>
    <SelectContent>
      {topicsBySubject[subject].map((topic) => (
        <SelectItem key={topic} value={topic}>{topic}</SelectItem>
      ))}
    </SelectContent>
  </Select>
);

export default TopicSelector;

// components/LessonDisplay.js
import React from 'react';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Volume2, VolumeX } from 'lucide-react';
import { useTTS } from '../hooks/useTTS';

const LessonDisplay = ({ lesson, subject, topic }) => {
  const { isSpeaking, handleSpeak, handleStopSpeaking } = useTTS();

  return (
    <Card className="mb-4">
      <CardHeader>
        <CardTitle>{subject}: {topic}</CardTitle>
      </CardHeader>
      <CardContent>
        <p>{lesson.content}</p>
      </CardContent>
      <CardFooter>
        <Button onClick={() => handleSpeak(lesson.content)} disabled={isSpeaking}>
          <Volume2 className="mr-2 h-4 w-4" /> Read Aloud
        </Button>
        {isSpeaking && (
          <Button onClick={handleStopSpeaking} variant="outline" className="ml-2">
            <VolumeX className="mr-2 h-4 w-4" /> Stop
          </Button>
        )}
      </CardFooter>
    </Card>
  );
};

export default LessonDisplay;

// components/ExerciseModal.js
import React, { useState } from 'react';
import { AlertDialog, AlertDialogAction, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from "@/components/ui/alert-dialog";
import { Input } from "@/components/ui/input";

const ExerciseModal = ({ isOpen, onClose, exercise, onSubmit }) => {
  const [userAnswer, setUserAnswer] = useState('');

  const handleSubmit = () => {
    onSubmit(userAnswer);
    setUserAnswer('');
    onClose();
  };

  return (
    <AlertDialog open={isOpen} onOpenChange={onClose}>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>{exercise?.question}</AlertDialogTitle>
        </AlertDialogHeader>
        <AlertDialogDescription>
          <Input
            type="text"
            placeholder="Your answer"
            value={userAnswer}
            onChange={(e) => setUserAnswer(e.target.value)}
          />
        </AlertDialogDescription>
        <AlertDialogFooter>
          <AlertDialogAction onClick={handleSubmit}>Submit Answer</AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
};

export default ExerciseModal;

// components/FeedbackDisplay.js
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const FeedbackDisplay = ({ feedback, discussion }) => (
  <>
    {feedback && (
      <Card className="mb-4">
        <CardHeader>
          <CardTitle>Exercise Feedback</CardTitle>
        </CardHeader>
        <CardContent>
          <p>{feedback}</p>
        </CardContent>
      </Card>
    )}
    {discussion && (
      <Card className="mb-4">
        <CardHeader>
          <CardTitle>Discussion Question</CardTitle>
        </CardHeader>
        <CardContent>
          <p>{discussion}</p>
        </CardContent>
      </Card>
    )}
  </>
);

export default FeedbackDisplay;

// hooks/useLesson.js
import { useState } from 'react';

export const useLesson = () => {
  const [lesson, setLesson] = useState(null);
  const [feedback, setFeedback] = useState('');
  const [discussion, setDiscussion] = useState('');

  const fetchLesson = async (subject, topic) => {
    // Mock API call - replace with actual API call in a real application
    const mockLesson = {
      content: `This is a sample lesson about ${topic} in ${subject}. In a real application, this content would be dynamically generated based on the selected subject and topic.`,
      exercise: {
        question: `Here's a practice question about ${topic} in ${subject}.`,
        answer: "Sample answer"
      }
    };
    setLesson(mockLesson);
    setFeedback('');
    setDiscussion('');
  };

  const checkAnswer = (userAnswer) => {
    // Mock API call - replace with actual API call in a real application
    setFeedback(`Your answer: "${userAnswer}" has been submitted. In a real application, this would be evaluated and proper feedback would be provided.`);
    setDiscussion(`Let's discuss more about ${lesson.exercise.question} What aspects of this topic do you find most interesting or challenging?`);
  };

  return { lesson, feedback, discussion, fetchLesson, checkAnswer };
};

// hooks/useTTS.js
import { useState } from 'react';

export const useTTS = () => {
  const [isSpeaking, setIsSpeaking] = useState(false);

  const handleSpeak = (text) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.onstart = () => setIsSpeaking(true);
      utterance.onend = () => setIsSpeaking(false);
      speechSynthesis.speak(utterance);
    } else {
      alert("Sorry, your browser doesn't support text-to-speech!");
    }
  };

  const handleStopSpeaking = () => {
    if ('speechSynthesis' in window) {
      speechSynthesis.cancel();
      setIsSpeaking(false);
    }
  };

  return { isSpeaking, handleSpeak, handleStopSpeaking };
};
