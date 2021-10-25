This project focused on creating quantum chess. We deliberated on many different ways on how to set up and store our positions for the chess pieces.
Ultimately, we decided that each chess piece would be assigned a 6 qubit register which would allow us to store its position in a multitude of states.
However, given that there are 32 pieces at the start of a chess game, this results in 192 qubits in total. Since we would be entangling the boards,
this is far too much data to store with current qiskit methods. 

We decided that sparse statevector representation would allow us to store all of our position data without overloading our simulation. We used components
from a quantum simulator we wrote a few months ago and adjusted it to work with row column data storage of sparse vectors. We are now able to store 
massive quantum states without much overhead (only about 12 kilobytes to store our chess board).

Additionally: we also calculated the math for modifying the position of our chess pieces (represented by a 64 value vector) into single and multiple state superpositions. This was done using unitary matrices that we calculated. However, we do not have a current implementation of it in the code. It is done using similar techniques that can be seen inside a hadamard gate.

Moving forward we plan to 1. implement conditional statements the player can write to decide what moves to make given certain outcomes of measurements, 2. verify the validity of moves and if they create unitary matrices, 3. write a display function that clearly communicates the information to the player, and 4. possibly implement turnwise piece entanglement. (5. GUI maybe)