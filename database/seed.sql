-- SmartAssist seed data (spec sections 4, 5, 21)
-- 3 subjects | 15 lessons | 75 resources (5 formats each) | 15 quizzes | 75 questions
-- Demo users and behaviour data (attempts/progress/recommendations) are
-- created by backend/app/seed.py at first application start.
-- Run only on an empty database: psql -d smartassist -f database/seed.sql

BEGIN;

INSERT INTO subjects (id, name, description) VALUES (1, 'Mathematics', 'Numbers, algebra and geometry fundamentals.');
INSERT INTO lessons (id, subject_id, title, description, difficulty, position) VALUES (1, 1, 'Number Systems', 'Natural numbers, integers, rational and irrational numbers.', 'EASY', 1);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (1, 1, 'TEXT', 'Normal Explanation', 'A number system is a way of writing numbers. Natural numbers are 1, 2, 3... Integers add 0 and negative numbers. Rational numbers can be written as a fraction p/q where q is not zero. Irrational numbers such as 2.1010010001... never end and never repeat.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (2, 1, 'SIMPLIFIED_TEXT', 'Simplified Explanation', 'Numbers come in groups. Counting numbers are 1, 2, 3. Add zero and negatives and you get integers. If a number can be written as a simple fraction it is rational. If it never stops and never repeats, it is irrational.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (3, 1, 'VISUAL', 'Visual Diagram', 'Number sets (smallest to largest):

   NATURAL  {1, 2, 3, ...}
     \n      INTEGER  {..., -1, 0, 1, ...}
         \n          RATIONAL  {1/2, 0.75, -3/4}
           + IRRATIONAL  {pi, sqrt(2)}
              =
           REAL NUMBERS', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (4, 1, 'AUDIO', 'Audio Explanation', 'Listen: Number systems group numbers. First come the counting numbers, then we add zero and negatives to make integers. Fractions give us rational numbers, and endless non-repeating decimals like pi are irrational. Together they form the real numbers.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (5, 1, 'SHORT_LESSON', 'Short Lesson', 'Number systems: counting numbers -> integers -> rationals + irrationals = real numbers. Key rule: a rational number can be written as a fraction; an irrational one cannot.', NULL);
INSERT INTO quizzes (id, lesson_id, title) VALUES (1, 1, 'Number Systems Quiz');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (1, 1, 'Which of these is an integer?', '-3.5', '-3', '1/2', '0.75', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (2, 1, 'Which number is irrational?', '0.5', '3/4', 'sqrt(2)', '-7', 'C');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (3, 1, 'Rational numbers can be written as...', 'decimals only', 'a fraction p/q', 'whole numbers', 'percentages', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (4, 1, 'Natural numbers start from...', '0', '-1', '1', '2', 'C');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (5, 1, 'Which set contains all the others?', 'Integers', 'Natural numbers', 'Real numbers', 'Fractions', 'C');
INSERT INTO lessons (id, subject_id, title, description, difficulty, position) VALUES (2, 1, 'Fractions and Decimals', 'Converting between fractions and decimals, comparing values.', 'EASY', 2);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (6, 2, 'TEXT', 'Normal Explanation', 'A fraction represents division: the numerator divided by the denominator. To convert a fraction to a decimal, divide numerator by denominator. For example 3/4 = 0.75. To convert a decimal to a fraction, write the decimal over a power of ten and simplify: 0.5 = 5/10 = 1/2.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (7, 2, 'SIMPLIFIED_TEXT', 'Simplified Explanation', 'A fraction is just division. 3/4 means 3 divided by 4, which equals 0.75. To turn a decimal into a fraction, put it over 10, 100 or 1000 and simplify. 0.5 becomes 5/10, then 1/2.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (8, 2, 'VISUAL', 'Visual Diagram', 'Fraction <-> Decimal conversion:

   1/2  --- divide -->  0.5
   3/4  --- divide -->  0.75
   1/5  --- divide -->  0.20

   0.25 --- 25/100 --> 1/4', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (9, 2, 'AUDIO', 'Audio Explanation', 'Listen: A fraction is a division sum. Top number divided by bottom number gives the decimal. 3 divided by 4 is 0.75. Going backwards, 0.5 is 5 over 10, which simplifies to one half.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (10, 2, 'SHORT_LESSON', 'Short Lesson', 'Fraction = division. Divide top by bottom for the decimal. For decimal to fraction, write over 10/100/1000 and simplify. 0.5 = 1/2, 0.75 = 3/4.', NULL);
INSERT INTO quizzes (id, lesson_id, title) VALUES (2, 2, 'Fractions and Decimals Quiz');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (6, 2, 'What is 3/4 as a decimal?', '0.34', '0.75', '0.33', '1.75', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (7, 2, 'What is 0.2 written as a fraction?', '1/2', '1/5', '2/100', '1/4', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (8, 2, 'Which is larger?', '3/5', '0.3', '1/2', '0.45', 'C');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (9, 2, 'Simplify 4/8:', '1/4', '2/4', '1/2', '4/2', 'C');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (10, 2, '0.125 equals...', '1/8', '1/4', '1/2', '125/10', 'A');
INSERT INTO lessons (id, subject_id, title, description, difficulty, position) VALUES (3, 1, 'Algebra Basics', 'Variables, expressions and simple substitution.', 'MEDIUM', 3);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (11, 3, 'TEXT', 'Normal Explanation', 'In algebra, letters such as x and y represent unknown values. An expression combines variables, constants and operations, e.g. 2x + 5. Substitution means replacing the variable with a number: if x = 3 then 2x + 5 = 2(3) + 5 = 11.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (12, 3, 'SIMPLIFIED_TEXT', 'Simplified Explanation', 'Algebra uses letters instead of numbers when we do not know the value yet. x + 3 means ''a number plus 3''. If you know x is 5, you swap it in: 5 + 3 = 8. That swap is called substitution.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (13, 3, 'VISUAL', 'Visual Diagram', 'Expression:   2x + 5
              |    |
          coefficient constant

Substitute x = 3:

   2(3) + 5 = 6 + 5 = 11', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (14, 3, 'AUDIO', 'Audio Explanation', 'Listen: In algebra a letter stands for a number we do not know yet. The expression 2x plus 5 means twice the number plus five. If x is three, put three in place of x and you get eleven.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (15, 3, 'SHORT_LESSON', 'Short Lesson', 'Letters = unknown numbers. 2x + 5 = twice x plus five. Substitute the known value to evaluate: x=3 gives 11. Coefficient is the number in front of the letter.', NULL);
INSERT INTO quizzes (id, lesson_id, title) VALUES (3, 3, 'Algebra Basics Quiz');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (11, 3, 'If x = 3, what is 2x + 5?', '8', '10', '11', '13', 'C');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (12, 3, 'In 4y, the coefficient is...', '4', 'y', '0', '1', 'A');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (13, 3, 'Which is an expression (not an equation)?', 'x + 2 = 5', '3x + 1', '2x/0', 'x = 9', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (14, 3, 'If a = 7, what is a - 2?', '5', '9', '7', '2', 'A');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (15, 3, 'Simplify 3x + 2x:', '5x', '6x', '5', '3x2', 'A');
INSERT INTO lessons (id, subject_id, title, description, difficulty, position) VALUES (4, 1, 'Linear Equations', 'Solving equations with one variable on both sides.', 'MEDIUM', 4);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (16, 4, 'TEXT', 'Normal Explanation', 'A linear equation has the variable to the power of one. To solve, isolate the variable: subtract 3 from both sides of x + 3 = 10 to get x = 7. Whatever you do to one side, do to the other. Check by substitution.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (17, 4, 'SIMPLIFIED_TEXT', 'Simplified Explanation', 'To find x, move everything else away. If x + 3 = 10, take 3 from both sides and x = 7. Always do the same thing to both sides so the equation stays balanced, like a scale.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (18, 4, 'VISUAL', 'Visual Diagram', 'Balanced equation scale:

   x + 3 = 10
   -3    -3     (subtract 3 both sides)
   -----------
     x   =  7

   Check: 7 + 3 = 10  OK', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (19, 4, 'AUDIO', 'Audio Explanation', 'Listen: Solving an equation is like balancing a scale. Keep both sides equal. If x plus three is ten, subtract three from both sides, and x is seven. Always check your answer.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (20, 4, 'SHORT_LESSON', 'Short Lesson', 'Isolate the variable. Same operation on both sides. x+3=10 -> subtract 3 -> x=7. Verify by substitution.', NULL);
INSERT INTO quizzes (id, lesson_id, title) VALUES (4, 4, 'Linear Equations Quiz');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (16, 4, 'Solve x + 3 = 10:', 'x = 13', 'x = 7', 'x = 3', 'x = 10', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (17, 4, 'Solve 2x = 12:', 'x = 6', 'x = 24', 'x = 10', 'x = 2', 'A');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (18, 4, 'Solve x - 4 = 5:', 'x = 9', 'x = 1', 'x = -1', 'x = 20', 'A');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (19, 4, 'Solve 3x + 2 = 11:', 'x = 3', 'x = 9', 'x = 4', 'x = 13', 'A');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (20, 4, 'To keep an equation balanced you must...', 'change only the left', 'change only the right', 'do the same to both sides', 'remove x', 'C');
INSERT INTO lessons (id, subject_id, title, description, difficulty, position) VALUES (5, 1, 'Geometry Essentials', 'Angles, triangles, perimeter and area.', 'HARD', 5);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (21, 5, 'TEXT', 'Normal Explanation', 'Geometry studies shapes, sizes and positions. Angles in a triangle sum to 180 degrees. The area of a rectangle is length x width; the perimeter is 2(l + w). The Pythagorean theorem states that for a right triangle a^2 + b^2 = c^2.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (22, 5, 'SIMPLIFIED_TEXT', 'Simplified Explanation', 'Geometry is about shapes. Triangle angles always add up to 180. Rectangle area = length times width. Perimeter is the distance around it: add all the sides. In a right triangle, a squared plus b squared equals c squared.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (23, 5, 'VISUAL', 'Visual Diagram', 'Right triangle (Pythagoras):

        |\ 
        | \  c
        |  \
     a  |___\
          b

   a^2 + b^2 = c^2

   Rectangle:  area = l x w,  P = 2(l+w)', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (24, 5, 'AUDIO', 'Audio Explanation', 'Listen: In geometry the angles of a triangle always add to one hundred eighty degrees. The area of a rectangle is length times width, and for right triangles a squared plus b squared equals c squared.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (25, 5, 'SHORT_LESSON', 'Short Lesson', 'Triangle angles = 180. Rectangle area = l x w; perimeter adds all sides. Right triangle: a^2 + b^2 = c^2.', NULL);
INSERT INTO quizzes (id, lesson_id, title) VALUES (5, 5, 'Geometry Essentials Quiz');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (21, 5, 'Angles in a triangle add up to...', '90', '180', '360', '270', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (22, 5, 'Area of a rectangle 5 x 3:', '15', '8', '30', '16', 'A');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (23, 5, 'A right triangle has angles of 90 and 40. Third angle:', '40', '50', '60', '130', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (24, 5, 'Perimeter of a 4 x 6 rectangle:', '10', '24', '20', '48', 'C');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (25, 5, 'If a=3, b=4, c (hypotenuse) = ?', '5', '6', '7', '12', 'A');
INSERT INTO subjects (id, name, description) VALUES (2, 'English', 'Grammar, sentence construction and vocabulary.');
INSERT INTO lessons (id, subject_id, title, description, difficulty, position) VALUES (6, 2, 'Parts of Speech', 'Nouns, verbs, adjectives, adverbs and their roles.', 'EASY', 1);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (26, 6, 'TEXT', 'Normal Explanation', 'English words are grouped into parts of speech. Nouns name people, places or things. Verbs express actions or states. Adjectives describe nouns (a bright star). Adverbs modify verbs, adjectives or other adverbs (she runs quickly). Pronouns replace nouns.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (27, 6, 'SIMPLIFIED_TEXT', 'Simplified Explanation', 'Parts of speech are word jobs. A noun names a thing, a verb shows action, an adjective describes a noun, and an adverb describes how an action happens. A pronoun like ''he'' replaces a name.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (28, 6, 'VISUAL', 'Visual Diagram', 'Word jobs:

   noun     ->  dog, Paris, idea
   verb     ->  run, is, think
   adjective->  happy, blue, tall
   adverb   ->  quickly, very, always
   pronoun  ->  he, she, it, they', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (29, 6, 'AUDIO', 'Audio Explanation', 'Listen: Every word has a job. Nouns name things, verbs show action, adjectives describe nouns, and adverbs tell us how something happens. Pronouns stand in for nouns so we do not repeat names.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (30, 6, 'SHORT_LESSON', 'Short Lesson', 'Noun = thing. Verb = action. Adjective describes a noun. Adverb describes an action. Pronoun replaces a noun.', NULL);
INSERT INTO quizzes (id, lesson_id, title) VALUES (6, 6, 'Parts of Speech Quiz');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (26, 6, 'Which is a noun?', 'quickly', 'happiness', 'run', 'blue-ish', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (27, 6, 'Which is a verb?', 'table', 'beautiful', 'jump', 'slowly', 'C');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (28, 6, '''She runs fast'' - ''fast'' is an...', 'noun', 'adjective', 'adverb', 'pronoun', 'C');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (29, 6, 'Which word is a pronoun?', 'dog', 'they', 'happy', 'eat', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (30, 6, 'An adjective usually describes a...', 'verb', 'noun', 'adverb', 'sentence', 'B');
INSERT INTO lessons (id, subject_id, title, description, difficulty, position) VALUES (7, 2, 'Tenses', 'Past, present and future verb forms.', 'MEDIUM', 2);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (31, 7, 'TEXT', 'Normal Explanation', 'Tenses tell when an action happens. Present tense describes now: ''I study''. Past tense describes before: ''I studied''. Future tense describes later: ''I will study''. Continuous forms show ongoing action: ''I am studying'', ''I was studying''.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (32, 7, 'SIMPLIFIED_TEXT', 'Simplified Explanation', 'Tenses show time. Now = present (I study). Before = past (I studied). Later = future (I will study). If something is still going on, use ''ing'': I am studying.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (33, 7, 'VISUAL', 'Visual Diagram', 'Timeline of tenses:

  PAST            PRESENT           FUTURE
  I studied   ->  I study       ->  I will study
  was reading    am reading        will be reading', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (34, 7, 'AUDIO', 'Audio Explanation', 'Listen: Tenses tell us when something happens. Study is now, studied is the past, will study is the future. Add ing when the action is still happening, like I am studying.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (35, 7, 'SHORT_LESSON', 'Short Lesson', 'Present: I study. Past: I studied. Future: I will study. Ongoing: I am/was/will be studying.', NULL);
INSERT INTO quizzes (id, lesson_id, title) VALUES (7, 7, 'Tenses Quiz');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (31, 7, '''I studied yesterday'' is which tense?', 'present', 'past', 'future', 'perfect', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (32, 7, 'Choose the future form: ''She ___ play.''', 'will', 'plays', 'played', 'playing', 'A');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (33, 7, '''They are eating'' is...', 'simple past', 'present continuous', 'future', 'past perfect', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (34, 7, 'Past tense of ''go'':', 'goed', 'gone', 'went', 'going', 'C');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (35, 7, '''I will have finished'' shows...', 'past', 'present', 'future', 'no time', 'C');
INSERT INTO lessons (id, subject_id, title, description, difficulty, position) VALUES (8, 2, 'Sentence Structure', 'Subject, verb and object; simple, compound and complex sentences.', 'MEDIUM', 3);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (36, 8, 'TEXT', 'Normal Explanation', 'A basic sentence follows subject + verb + object: ''The cat (S) chased (V) the mouse (O).'' A simple sentence has one independent clause. A compound sentence joins two clauses with and, but or or. A complex sentence adds a dependent clause such as ''Because it rained''.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (37, 8, 'SIMPLIFIED_TEXT', 'Simplified Explanation', 'Sentences need who (subject), did what (verb), and to what (object). One idea = simple. Two ideas joined with and/but = compound. One main idea plus a small extra idea = complex.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (38, 8, 'VISUAL', 'Visual Diagram', 'Simple:    [The cat] [chased] [the mouse]
              S          V         O

Compound:  [I stayed] + and + [it rained]

Complex:   [Because it rained] , [I stayed home]', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (39, 8, 'AUDIO', 'Audio Explanation', 'Listen: Every sentence needs a subject and a verb, and often an object. The cat chased the mouse. Join two complete ideas with and or but to make a compound sentence.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (40, 8, 'SHORT_LESSON', 'Short Lesson', 'S + V + O is the core. Simple = one idea. Compound = two ideas joined. Complex = main idea + ''because/when/which'' clause.', NULL);
INSERT INTO quizzes (id, lesson_id, title) VALUES (8, 8, 'Sentence Structure Quiz');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (36, 8, 'In ''Rita wrote a letter'', the object is...', 'Rita', 'wrote', 'a letter', 'none', 'C');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (37, 8, 'A compound sentence joins clauses with...', 'because', 'and/but/or', 'which', 'that', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (38, 8, '''Because it rained, we stayed'' is a...', 'simple', 'compound', 'complex', 'fragment', 'C');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (39, 8, 'Which part is the verb?', 'dog', 'barked', 'loudly', 'yard', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (40, 8, 'Every sentence must contain at least...', 'an adjective', 'a subject and a verb', 'an object', 'a comma', 'B');
INSERT INTO lessons (id, subject_id, title, description, difficulty, position) VALUES (9, 2, 'Active and Passive Voice', 'Changing sentence focus from doer to receiver.', 'HARD', 4);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (41, 9, 'TEXT', 'Normal Explanation', 'Active voice: the subject performs the action - ''Ravi wrote the essay.'' Passive voice: the subject receives the action - ''The essay was written by Ravi.'' Form: object + past participle (+ by + subject). Passive is useful when the doer is unknown or unimportant.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (42, 9, 'SIMPLIFIED_TEXT', 'Simplified Explanation', 'Active: the doer comes first. Ravi wrote the essay. Passive: the thing done comes first. The essay was written by Ravi. Flip the sentence so the object leads.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (43, 9, 'VISUAL', 'Visual Diagram', 'ACTIVE:   Ravi  wrote  the essay
             S      V       O

   flip ---------^^^

PASSIVE:  The essay was written by Ravi
             S            V       by-agent', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (44, 9, 'AUDIO', 'Audio Explanation', 'Listen: In active voice the doer acts. Ravi wrote the essay. In passive voice the receiver leads. The essay was written by Ravi. Use passive when the doer does not matter.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (45, 9, 'SHORT_LESSON', 'Short Lesson', 'Active = doer first. Passive = receiver first, verb = was/were + past participle. Use passive when the agent is unknown or unimportant.', NULL);
INSERT INTO quizzes (id, lesson_id, title) VALUES (9, 9, 'Active and Passive Voice Quiz');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (41, 9, 'Passive of ''Mina cleaned the room'':', 'Mina cleaned the room', 'The room was cleaned by Mina', 'The room cleaned Mina', 'The room is cleaning Mina', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (42, 9, 'Active voice puts the ___ first.', 'object', 'doer', 'verb', 'adjective', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (43, 9, 'Passive form uses...', 'only past tense', 'was/were + past participle', 'will', 'ing only', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (44, 9, 'Passive is useful when the doer is...', 'known', 'important', 'unknown', 'always named', 'C');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (45, 9, '''The ball was kicked by Sam'' is...', 'active', 'passive', 'compound', 'question', 'B');
INSERT INTO lessons (id, subject_id, title, description, difficulty, position) VALUES (10, 2, 'Vocabulary Building', 'Synonyms, antonyms, prefixes and word roots.', 'EASY', 5);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (46, 10, 'TEXT', 'Normal Explanation', 'Vocabulary grows by learning synonyms (big/large), antonyms (big/small), prefixes (un-, re-, pre-) and roots. For example ''unhappy'' = un + happy, ''rewrite'' = re + write. Reading widely and noting new words in context is the fastest way to improve.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (47, 10, 'SIMPLIFIED_TEXT', 'Simplified Explanation', 'Words have partners: synonyms mean the same (big = large), antonyms mean the opposite (big = small). Little word parts change meaning: un- makes it opposite, re- means again. Read a lot and guess new words from the sentence.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (48, 10, 'VISUAL', 'Visual Diagram', 'Word building:

   un + happy  = unhappy   (opposite)
   re + write  = rewrite   (again)
   pre + view  = preview   (before)

   synonyms:  big = large
   antonyms:  big = small', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (49, 10, 'AUDIO', 'Audio Explanation', 'Listen: To grow your vocabulary, learn word families. Synonyms are words with the same meaning, antonyms the opposite. Prefixes like un and re change the meaning: unhappy, rewrite.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (50, 10, 'SHORT_LESSON', 'Short Lesson', 'Synonym = same, antonym = opposite. Prefixes un/re/pre change meaning. Learn words from context while reading.', NULL);
INSERT INTO quizzes (id, lesson_id, title) VALUES (10, 10, 'Vocabulary Building Quiz');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (46, 10, 'Synonym of ''large'':', 'tiny', 'big', 'thin', 'short', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (47, 10, 'Antonym of ''begin'':', 'start', 'end', 'open', 'go', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (48, 10, '''Unhappy'' means...', 'very happy', 'not happy', 'again happy', 'before happy', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (49, 10, '''Rewrite'' means to write...', 'once', 'again', 'badly', 'before', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (50, 10, 'A prefix is added at the...', 'end', 'middle', 'beginning', 'none', 'C');
INSERT INTO subjects (id, name, description) VALUES (3, 'Computer Science', 'Computing fundamentals: binary, data structures, algorithms and databases.');
INSERT INTO lessons (id, subject_id, title, description, difficulty, position) VALUES (11, 3, 'Binary Numbers', 'Base-2 number system used by computers.', 'EASY', 1);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (51, 11, 'TEXT', 'Normal Explanation', 'Binary numbers use only two digits: 0 and 1. Computers store everything as binary because electronic switches have two states, off and on. Each binary digit is a bit; eight bits form a byte. The place values are powers of two: 1, 2, 4, 8, 16. So 1011 in binary = 8 + 0 + 2 + 1 = 11 in decimal.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (52, 11, 'SIMPLIFIED_TEXT', 'Simplified Explanation', 'Binary is a number system that uses only 0 and 1. Each position counts double the one before: 1, 2, 4, 8. To read 1011, add the places with a 1: 8 + 2 + 1 = 11. Computers like binary because a switch can be off (0) or on (1).', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (53, 11, 'VISUAL', 'Visual Diagram', 'Binary place values (4 bits):

   1    0    1    1
   8    4    2    1
   ^         ^  ^
   8    +    2 + 1  =  11 in decimal

   Switches:  [OFF] [ON] [OFF] [ON]  -> 0 1 0 1', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (54, 11, 'AUDIO', 'Audio Explanation', 'Listen: Binary uses only zero and one. Each place is worth twice the place to its right: one, two, four, eight. In one zero one one, add eight, two and one to get eleven.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (55, 11, 'SHORT_LESSON', 'Short Lesson', 'Binary = 0 and 1 only. Places: 1, 2, 4, 8. 1011 = 8+2+1 = 11. One digit = one bit; 8 bits = 1 byte.', NULL);
INSERT INTO quizzes (id, lesson_id, title) VALUES (11, 11, 'Binary Numbers Quiz');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (51, 11, 'What digits are used in binary?', '0 and 1', '1 and 2', '0 to 9', 'A and B', 'A');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (52, 11, 'What is 1011 in decimal?', '9', '11', '13', '1011', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (53, 11, 'One binary digit is called a...', 'byte', 'bit', 'nibble', 'word', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (54, 11, 'How many bits in one byte?', '4', '8', '16', '32', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (55, 11, 'The binary place to the left of 1 is...', '2', '4', '8', '0', 'A');
INSERT INTO lessons (id, subject_id, title, description, difficulty, position) VALUES (12, 3, 'Data Structures', 'Arrays, linked lists, stacks, queues and trees.', 'MEDIUM', 2);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (56, 12, 'TEXT', 'Normal Explanation', 'A data structure organises data for efficient use. Arrays store items in contiguous memory with fast index access O(1) but costly insertions. Linked lists store nodes with pointers, making insertion cheap but access O(n). Stacks are LIFO (last in first out), queues are FIFO. Trees organise data hierarchically for fast search O(log n).', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (57, 12, 'SIMPLIFIED_TEXT', 'Simplified Explanation', 'A data structure is a way of arranging data. An array is a row of numbered boxes - fast to read by position. A linked list is boxes joined by arrows. A stack is like a pile of plates (last one on, first one off). A queue is a line of people (first in, first out).', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (58, 12, 'VISUAL', 'Visual Diagram', 'Array:      [10][20][30][40]   index 0..3

Linked list: (10)->(20)->(30)->NULL

Stack (LIFO):      Queue (FIFO):
   [30] top           front->[10]  [20] [30]<-back
   [20]               first out = 10 (first in)
   [10]', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (59, 12, 'AUDIO', 'Audio Explanation', 'Listen: Data structures arrange data. Arrays are numbered boxes, fast to reach by index. Linked lists connect nodes with pointers. Stacks are last in first out, queues first in first out.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (60, 12, 'SHORT_LESSON', 'Short Lesson', 'Array = fixed boxes, fast access. Linked list = nodes with arrows. Stack = LIFO. Queue = FIFO. Tree = branching, fast search.', NULL);
INSERT INTO quizzes (id, lesson_id, title) VALUES (12, 12, 'Data Structures Quiz');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (56, 12, 'Which structure is LIFO?', 'Queue', 'Stack', 'Array', 'Tree', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (57, 12, 'Which structure is FIFO?', 'Stack', 'Queue', 'Tree', 'Graph', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (58, 12, 'Array element access is typically...', 'O(1)', 'O(n)', 'O(log n)', 'O(n^2)', 'A');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (59, 12, 'A linked list node stores data plus...', 'an index', 'a pointer to next', 'a stack', 'a queue', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (60, 12, 'Which is a hierarchical structure?', 'Queue', 'Stack', 'Tree', 'Array', 'C');
INSERT INTO lessons (id, subject_id, title, description, difficulty, position) VALUES (13, 3, 'Algorithms', 'Step-by-step procedures, search and sorting.', 'MEDIUM', 3);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (61, 13, 'TEXT', 'Normal Explanation', 'An algorithm is a finite sequence of steps that solves a problem. Linear search checks each item: O(n). Binary search halves the search each step on sorted data: O(log n). Sorting algorithms include bubble sort O(n^2) and merge sort O(n log n). Good algorithms are correct, efficient and clear.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (62, 13, 'SIMPLIFIED_TEXT', 'Simplified Explanation', 'An algorithm is a recipe for solving a problem. Linear search looks at every item one by one. Binary search is smarter: look in the middle, then discard half. Sorting can be done by repeatedly swapping neighbours (bubble) or splitting and merging (merge sort).', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (63, 13, 'VISUAL', 'Visual Diagram', 'Binary search on sorted data (target 30):

  [10][20][30][40][50][60][70]
         ^mid = 40 -> 30 is left, discard right

  [10][20][30]
       ^mid = 20 -> go right
        [30]  FOUND', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (64, 13, 'AUDIO', 'Audio Explanation', 'Listen: An algorithm is a clear list of steps. Linear search checks everything. Binary search checks the middle and throws away half the list each time, so it is much faster on sorted data.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (65, 13, 'SHORT_LESSON', 'Short Lesson', 'Algorithm = finite steps to solve a problem. Linear search O(n), binary search O(log n) on sorted data. Bubble sort O(n^2), merge sort O(n log n).', NULL);
INSERT INTO quizzes (id, lesson_id, title) VALUES (13, 13, 'Algorithms Quiz');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (61, 13, 'Binary search requires the data to be...', 'unsorted', 'sorted', 'numeric', 'small', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (62, 13, 'Linear search time complexity is...', 'O(1)', 'O(log n)', 'O(n)', 'O(n log n)', 'C');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (63, 13, 'Binary search works by...', 'checking all', 'halving the range', 'sorting first', 'random pick', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (64, 13, 'Which sorting splits and merges?', 'Bubble sort', 'Selection sort', 'Merge sort', 'Insertion sort', 'C');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (65, 13, 'An algorithm must be...', 'infinite', 'finite and defined', 'written in Java', 'random', 'B');
INSERT INTO lessons (id, subject_id, title, description, difficulty, position) VALUES (14, 3, 'Programming Loops', 'for, while and control flow in programs.', 'MEDIUM', 4);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (66, 14, 'TEXT', 'Normal Explanation', 'A loop repeats a block of code. A for loop runs a known number of times: for i in range(5). A while loop repeats while a condition is true - beware infinite loops if the condition never becomes false. break exits the loop; continue skips to the next iteration. Nested loops run a loop inside another loop.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (67, 14, 'SIMPLIFIED_TEXT', 'Simplified Explanation', 'Loops save you from writing the same code again and again. Use for when you know how many times to repeat, and while when you repeat until something changes. Always make sure the loop can end, or it runs forever.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (68, 14, 'VISUAL', 'Visual Diagram', 'for loop flow:

   start -> condition -> body -> update -> condition ...
                | false
                v
              end

   for i in 1..3:  print i   ->  1, 2, 3', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (69, 14, 'AUDIO', 'Audio Explanation', 'Listen: A loop repeats code. A for loop runs a set number of times. A while loop keeps going while its condition stays true. Make sure something inside the loop eventually changes, or it never stops.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (70, 14, 'SHORT_LESSON', 'Short Lesson', 'for = known count; while = repeat until condition changes. Watch for infinite loops. break exits, continue skips ahead.', NULL);
INSERT INTO quizzes (id, lesson_id, title) VALUES (14, 14, 'Programming Loops Quiz');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (66, 14, 'A for loop is best when the count is...', 'unknown', 'known', 'zero', 'random', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (67, 14, 'An infinite loop happens when...', 'the condition never ends the loop', 'you use break', 'count is 5', 'nested', 'A');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (68, 14, '''break'' does what?', 'skips iteration', 'exits the loop', 'restarts program', 'prints', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (69, 14, '''continue'' does what?', 'exits loop', 'skips to next iteration', 'stops program', 'deletes', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (70, 14, 'Which repeats while a condition is true?', 'for', 'while', 'if', 'return', 'B');
INSERT INTO lessons (id, subject_id, title, description, difficulty, position) VALUES (15, 3, 'Database Basics', 'Tables, keys, relations and simple SQL.', 'HARD', 5);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (71, 15, 'TEXT', 'Normal Explanation', 'A relational database stores data in tables of rows and columns. Each row is a record; a primary key uniquely identifies it. Foreign keys link tables, creating relations (one student many attempts). Normalisation removes duplication. SQL statements: CREATE, INSERT, SELECT, UPDATE, DELETE. ACID guarantees reliable transactions.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (72, 15, 'SIMPLIFIED_TEXT', 'Simplified Explanation', 'A database is a set of tables. Each table has rows (records) and columns (fields). A primary key is a unique ID for each row. A foreign key is an ID that points to another table, linking them. SQL is the language used to ask the database questions.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (73, 15, 'VISUAL', 'Visual Diagram', 'users                    attempts
+----+-------+           +----+---------+--------+
| id | name  |           | id | student | score  |
+----+-------+           +----+---------+--------+
|  1 | Rahul |<----------|  1 |    1    |  80%   |
+----+-------+  FK        +----+---------+--------+

   SELECT * FROM attempts WHERE score > 50;', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (74, 15, 'AUDIO', 'Audio Explanation', 'Listen: A database stores data in tables. Rows are records, columns are fields. Primary keys identify rows, foreign keys link tables. SQL lets you create, read, update and delete data.', NULL);
INSERT INTO resources (id, lesson_id, type, title, content, media_url) VALUES (75, 15, 'SHORT_LESSON', 'Short Lesson', 'Tables = rows + columns. Primary key = unique ID. Foreign key = link to another table. SQL: CREATE, SELECT, UPDATE, DELETE. ACID = safe transactions.', NULL);
INSERT INTO quizzes (id, lesson_id, title) VALUES (15, 15, 'Database Basics Quiz');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (71, 15, 'A primary key is...', 'duplicated', 'unique', 'optional', 'text only', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (72, 15, 'A foreign key...', 'uniquely identifies rows', 'points to another table', 'encrypts data', 'deletes rows', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (73, 15, 'Which SQL statement reads data?', 'DELETE', 'SELECT', 'DROP', 'TRUNCATE', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (74, 15, 'A row in a table is a...', 'field', 'record', 'key', 'schema', 'B');
INSERT INTO questions (id, quiz_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (75, 15, 'ACID describes...', 'queries', 'transaction safety', 'indexes only', 'keys', 'B');

-- Demo accounts (passwords are PBKDF2 hashes; app/seed.py creates them too)
COMMIT;
