# Snake-AI-Neural-Network
#### Genetic Algorithm
![ga](https://user-images.githubusercontent.com/25164326/50758931-94c2c280-1231-11e9-946c-6af22322d118.gif)

#### Brute-Force Randomization Learning
![bf](https://user-images.githubusercontent.com/25164326/50758934-97251c80-1231-11e9-93c6-dc5b444633ba.gif)

## Problem Statement

We sought to build a neural network  capable of learning how to solve a simple game; Here definition of &quot;solve&quot; involved training the AI to perform at a level comparable to the average human player, if not better. To be more specific,we defined an average score of 10 or more apples consumed per 100 games to be considered &quot;solved&quot;.

In this instance we built a simple Snake game based on the classic Snake games many of us have seen on old Nokia phones. Our decision was justified by the fact that the inputs in this game are fairly simple, with only 3 actions that a snake can make at any given time (move left, move forward, move right). At the same time, the player needs to garner enough knowledge of the problem space that the game cannot simply be solved using random inputs. Additionally, since the game does not require an adversary, it can be trained against itself using a methodology centered around &quot;self improvement&quot;.

## Neural Network Architectures

We opted to explore two Neural Network architectures to implement a self-learning, game- playing AI: they were &quot;brute-force&quot; based reinforcement learning, and &quot;genetic algorithm&quot; based reinforcement learning.

We consider &quot;brute-force&quot; to be a neural network that is trained on a number of randomly generated training data with reinforcement labels. Similarly to other neural networks we&#39;ve explored, this one is trained using backpropagation. Moreover, each element in the training set is built to only look ahead by one step. This means that the brute-force neural network should operate in a very greedy fashion, without really looking ahead towards multiple actions.

We&#39;ve complemented the brute-force neural network with a genetic algorithm based neural network. Unlike brute-force, our genetic neural network does not learn using back propagation but instead uses a combination of natural selection, breeding, and mutation to generate a trained neural network. We initially hypothesised  that it would take longer to train, but would have the capacity to outperform the brute-force implementation. We theorize that the genetic algorithm has the potential to learn traits that aren&#39;t explicitly trained using the brute-force implementation. We also believe that this approach is less likely to overfit than brute-force.

## Brute-Force Randomization Learning Neural Network

The brute-force neural network learns by building a randomized training dataset paired with reinforcement training labels. This is performed by essentially running the game and then generating a random action and its associated reinforcement label for each step. We consider 3 possible labels of reinforcement--positive, neutral, and negative. An input is considered positive reinforcement when it causes the snake agent to either increase its score by consuming an apple, or by decrease its distance to the apple. We negatively reinforce the network when an action will result in and end game state. For instance, choosing an action that would result in bumping into the edge of the screen, or another part of the snake is negatively reinforced. All other actions are considered neutral reinforcements.

### Neural Network Architecture

We&#39;ve opted to use 5 inputs to our neural network. These include 3 boolean values representing an obstacle to the left, front, or right of the agent, the agent&#39;s angle to the food, and the action the agent can take [3]. This action represents the direction the snake can move. It is very important to use input values that best represent the agent&#39;s possible choices with respect to the goal. We noticed that incorrectly providing the angle of the agent to the food resulted in a model that was unable to correctly train.

Our neural network had a single hidden layer with 75 neurons, where all the neurons are activated by the rectified linear (ReLU) unit function. We also opted to use a single output to our neural network with a value between 0 and 1, where 0 represents no action to be taken and 1 represents an action to be taken. To decide which direction the agent should take we calculate a set of 3 predictions for each possible action (move left, move forward, move right) and calculate the argmax of all 3 inputs to select the action that has highest stenge to be taken. To get a value between 0 and 1 we needed to make sure that the output layer needed to be activated by the sigmoid activation function.

Finally, we trained the neural network by performing back propagation on our set of randomly generated training data and associated reinforcement labels by minimizing the loss (seen in Figure - 7) which was found using the root mean square function and adjusting the weights with a learning rate of 0.01.

![1](https://user-images.githubusercontent.com/25164326/50759302-a6f13080-1232-11e9-8045-6bd9befd3c69.png)
##### Figure-1: Brute-Force Neural Network Architecture

We experimented with a number of different hyperparameters, including different hidden sizes of neurons in our hidden layers, different number of hidden layers, different activation functions, and finally different initial weight distributions. On the whole,we noticed an interesting trend that was quite different than the trends we had previously seen in our assignments. In almost all cases, a fewer number of hidden layers and neurons were required than we had expected. The more complexity we introduced, the more opportunities there were to overfit our data.

### Building Training Data

To build our training data, we would iterate over a number of games, for example 10, 100, 100, 1000, or 1000 games, each game averaging around 170 frames. With each game, we would randomly select the next action (move left, forward, right) on every single frame and calculate whether or not it would prove a positive action. The specific constraint we defined is was the distance to the food as smaller than the previous position, or a score  greater than the previous score. We also generated negative associations for scenarios that would result in an end game state, and neutrally reinforce actions that would result in the agent being farther away from the food. As we opted to return an output between -1 and 1 we decided to input training reinforcement labels of -1, 0, and 1. After each iteration we store the newly created training input and label into the training dataset.

### Training Methodology

We initialize our neural network with uniform a random distribution of weights. We then opted to run the neural network for 10 - 15 epochs with a batch of 32.

## Genetic Algorithm Neural Network

In contrast to the brute-force neural networks&#39; reliance on backpropagation, our genetic algorithm based neural network adjusts its weight and bias via number of genetic functions. These include natural selection, mutation, and the evolution of top ranked neural network models. The system operates by generating N models, selecting the top K, then finally breeding and mutating the remaining N-K models on each generation.

Similarly to the brute-force neural network, we needed to have a methodology of ranking each of the models at the end of a generation to select which models are kept and which ones are discarded. Consequently, we designed a fitness function based on a number of attributes and corresponding scoring factors. These include the score of the agent (the apple&#39;s consumed in a single life), the angle towards the food, and the distance to the food. Each of these attributes are scaled differently based on their importance. We see having a higher player score as more important than the angle towards the food, thus it yields a higher weight due to a higher scoring factor.

### Neural Network Architecture

We found that our underlying neural network architecture for the brute-force neural network worked very well for our genetic algorithm architecture, and opted to use it once again for our genetic neural network. Both the inputs and outputs of the neural network are identical as the problem the agent faces is identical to our brute-force neural network.

Similarly to our brute-force implementation we&#39;ve opted to use 5 inputs corresponding to the presence of an obstacle to the left, in front of, or to the right of the agent, the agent&#39;s angle to the food, and the action the agent took (moving left, forward, right). Our output once again a single value between 0 and 1, where 0 corresponds to no action and 1 to taking action. For each step the agent takes we calculate the prediction of the agent taking any 3 of the actions and selecting the one with output closest to 1. The single difference to our brute-force architecture is the use of 25 hidden neurons versus 75 (Figure - 9 shows the Computational Graph for the brute-force neural network). We wished to keep the number of hidden neurons small as having a larger number of neurons would correspond to a larger number of weights to be bred and mutated.

Finally we opted to use a uniform random distribution of weights as we found that high variation between -1 and 1 yielding the best initial results for our neural network. For both the brute-force and genetic neural network we would often get stuck in local optimum positions, even on our genesis generation. For example it appeared more common for our agent to enter a cyclical loop of output actions (move left, left, left, left, etc) given its set of input values corresponding to those positions. We found that our random normal distribution of initial weights performed more poorly in our use case than our uniform random distribution of initial weights. The diagram below visualizes the random normal distributions tendency to get stuck at a poor local optimum.

![2](https://user-images.githubusercontent.com/25164326/50759304-a9538a80-1232-11e9-8010-abb4dac72f7e.png)
##### Figure-2: Genetic Neural Network Scores vs different Neural Network weight initializations

### Training Methodology

We needed to build a system of genetic evolution over a series of generations as the genetic neural network did not rely on training data to train, like the brute-force model. This generation system consists of selecting the models with the highest fitness, then breeding and mutating them to build our next generation. Our generation system operates on the following algorithm:

1. Initialize N randomized networks using uniform random distribution for weights and biases
2. Run a round of the game until all N snakes fail or reach a timeout period
3. Rank each of the models by their fitness function
4. If all models are stuck at a local optimum, purge the generation and start from a new genesis
  1. Necessary of all neurons have fallen into a local optimum
5. Select the top K models
6. Fill the remaining N-K slots with newly bred and mutated models
  1. Breed the remaining N-K models from ideal parents
  2. Randomly mutate the remaining N-K models by a mutation factor

This algorithm over time generates models that more and more closely reach our goal of a &quot;solved&quot; AI for the snake game. To achieve this we perform breeding and mutation. In our implementation we consider mutation the random adjustment of individual weights of a given model by a mutation scaling factor. We define this as [1]:

        _1 + ((random.random() - 0.5) \* 3 + (random.random() - 0.5))_

We also opt to breed two models together to get a possibly better performing model. To achieve the highest number of successful candidate models we breed a child from two parents, the first parent from our top K elements and the second parent from any of the N elements from the previous generation. This combination guarantees that every newly generated model contains positive features from the best of the previous generation, while preventing it from falling too deep into a local optimum.

There are a number of factors necessary to prevent us from falling into local optimum. First we opt to purge any generations that essentially evolve themselves into a corner, following strategies that keep them alive early but don&#39;t allow them to progress towards the end goal of &quot;solving&quot; the goal of self playing AI. For example we would often see agents avoiding the boundaries of the game, and thus staying alive the longest, but instead would never pursue the apple for a higher fitness. Finally to make sure that our best performing agents continue to perform well, we have opted not to mutate any of our top K models, but instead opt to only mutate a subset our newly bred N-K models.

### Testing Methodology

We&#39;ve run a series of tests that compare a number of hyperparameters of both our brute-force and genetic neural network implementations. In our problem statement we noted our classification for &quot;solving&quot; our game playing AI would be to achieve an average score of above 10. For each of our tests below we&#39;ve opted to calculate an average and max player score over a total of 100 games. For example we train the brute-force neural network over 10,000 games, and then test the resulting model by calculating its average and high score over 100 &quot;test&quot; games.

#### Brute-Force Testing Validation Scores:

The brute-force model performed best for both average and high scores after training over 100 games. We noticed that this trend began to decline after 1,000 games. We believe this is due to overfitting our training dataset.

![3](https://user-images.githubusercontent.com/25164326/50759307-aa84b780-1232-11e9-909d-ab1e35de844b.png)
##### Figure-3: (5, 75, 1) Brute-Force Neural Network Scores vs Number of games played

![4](https://user-images.githubusercontent.com/25164326/50759310-abb5e480-1232-11e9-9b34-d9a6bbd2e8a5.png)
##### Figure-4: Brute-Force Neural Network Scores vs Different Neural Network Architecture

#### Genetic Algorithm Testing Validation Scores

![5](https://user-images.githubusercontent.com/25164326/50759311-ad7fa800-1232-11e9-934e-e1a6877db33e.png)
##### Figure-5: Genetic Algorithm Neural Network Scores vs Number of Snake generation

## Conclusion

We were faced with a number of difficult challenges throughout the process of understanding and implementing both the brute-force and the genetic neural network, such as the importance of supplying useful input parameters to the neural network. In conclusion we believe we produced a series of models that were capable of correctly &quot;solving&quot; our problem statement.

## Implementation Challenges

The most important lesson learned while working on this project is that the input data that needs to be fed into the neural network has to make logical sense.If coherent logic cannot be used to successfully map a function that the neural network is trying to achieve, it will refuse to learn.

While using the brute force reinforcement algorithm, the data provided were awareness of obstacles to its left, front and right, the random direction chosen by the random number generator and the euclidean distance from the head of the snake to the food. Using these input data the neural network failed to map the function where it needed to avoid, the walls, itself and approach the food. With this data all that the neural network did was go in a continuous circular direction as it thought that was the best way to survive and had no idea of how it would approach the food.In order to fix this problem, the euclidean distance between the snake&#39;s head and food was replaced by the angle from the head of the snake and the food.

## Optimum Architecture

That being said we believe that we&#39;ve satisfied our initial problem statement of &quot;solving&quot; the game playing neural network via our brute-force neural network architecture. While we were able to train a game playing AI using the genetic algorithm, we found its learning rate and efficiency were below our defined average 10 score. For this reason we opt to use the brute-force neural network at this time.

### Instructions on running

Requires Python 3 with the following modules below installed:
* pygame 
* numpy
* math
* keras
* random
* tqdm
* time
* os
* scipy

After installing the modules go into the directory and simply type in:

```sh
$ python __main__.py
```
License
----

MIT


**THanks for checking this out!**
