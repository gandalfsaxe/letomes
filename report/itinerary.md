
# General structure and talking points (LETOMES)
* **Introduction**
* **Background/Relevant Literature** *(Including Gandalf's BSc project)*
* **Analysis** *(Here, we formulate our hypotheses, and generally give a before-the-fact run-down of what the project and report will be like.)*
    * **Errors we found in the old code** *(We found some mathematical errors in the old code; argue for why they don't invalidate the old results.)*
    * **Math** *(Hamiltonian mechanics, symplectic verlet, derivations, all that stuff)*
    * **Evolution Strategies** *(all our machine learning considerations. Formal definition of ES algorithm and how it relates to its variants and competitors)*
    * **High-performance computing** *(as it relates to ES with an expensive objective function)*
        * **Pagmo** *(making the case for parallelism, given that trajectories are independent, and explaining the metaphor behind pagmo, and why we think it useful)*
        * **GPU/CUDA programming** *(massive parallelism vs. data transfer overhead)*
    * **Software Engineering** *(incl. working with old code, mutability/performance tradeoff)*
        * **Unit testing** *(ensuring correctness of complex system with many edits taking place)*
* **Implementation and Results** 
    * **Program architecture** *(for the simulator/integrator)*
    * **ES model**
        * **hyperparameters**
        * **adaptive measures** *(e.g. less precise paths for the gradient estimation step than for the candidate points themselves)*, 
        * **trial and error** *(finding a model that worked)*
    * **Best trajectories** *(and how long it took to find them)*
* **Discussion**
    * **Validity of trajectories: Lyapunov exponent** *(argue for correctness of method and trustworthiness of trajectories by quantifying the inherent chaos: Basically, we are addressing the fact that this is a numerical simulation, and therefore a compressed view of the real thing. It is important to argue that that compression is not too much)*
    * **Usefulness of ES** *(how well does it compare to the old brute-force method? Do we get anything out of estimating a gradient? Do our results' quality scale with a more complex model? (more noise points, more annealing))*
    * **Inspect the tradeoff between $\Delta v$ and duration** *(plot this, if we can get enough different successful trajectories. What does that plot look like?)*
    * **Performance Optimization** *(was Pagmo a good choice? Is it a reasonable problem to run on GPU or are we transporting too much data?*
    * **Self-evaluation** *(Was our time well spent? Did we gain anything from our "reinventing the wheel", reimplementing the lunar simulator? Should we have focused on running on the old code without delving into it?)*
* **Conclusion**
* **Acknowledgements/Appendix etc.**