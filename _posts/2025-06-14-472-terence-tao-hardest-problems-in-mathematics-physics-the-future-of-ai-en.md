---
layout: post
title: "472 - Terence Tao: Hardest Problems in Mathematics, Physics & the Future of AI"
date: 2025-06-14 09:00:00 +0000
article_id: 472-terence-tao-hardest-problems-in-mathematics-physics-the-future-of-ai
article_title: "472 - Terence Tao: Hardest Problems in Mathematics, Physics & the Future of AI"
collection_id: lex-fridman
language: en
variant_rank: 1
original_link: "https://www.youtube.com/watch?v=HUkBz-cdB-k"
excerpt: "Terence Tao, widely regarded as one of the most brilliant mathematicians of the modern era, has achieved a rare distinction in the world of mathematics. Often hailed as the \"Mozart of math,\" Tao has not only made profound contributions across a vast array of mathematical disciplines but has also earned the highest honors in the field, including the Fields Medal and the Breakthrough Prize. His intellectual reach spans number theory, harmonic analysis, partial differential equations, combinatorics, and mathematical physics—areas that, at first glance, seem unrelated. Yet Tao’s work reveals a deep underlying unity in mathematical structure, where insights from one domain illuminate problems in another."
permalink: /articles/472-terence-tao-hardest-problems-in-mathematics-physics-the-future-of-ai/en/
---


### **A Deep Exploration of Mathematical Thought: The Mind of Terence Tao**

Terence Tao, widely regarded as one of the most brilliant mathematicians of the modern era, has achieved a rare distinction in the world of mathematics. Often hailed as the "Mozart of math," Tao has not only made profound contributions across a vast array of mathematical disciplines but has also earned the highest honors in the field, including the Fields Medal and the Breakthrough Prize. His intellectual reach spans number theory, harmonic analysis, partial differential equations, combinatorics, and mathematical physics—areas that, at first glance, seem unrelated. Yet Tao’s work reveals a deep underlying unity in mathematical structure, where insights from one domain illuminate problems in another.

This detailed third-person paraphrase explores the full breadth of a conversation with Tao, drawing on his reflections on mathematical discovery, the nature of difficult problems, the role of intuition and collaboration, and the evolving relationship between mathematics and artificial intelligence. The narrative is structured to preserve the original depth and nuance while rephrasing the content in a formal, analytical tone suitable for academic and intellectual audiences.

---

### **1. The Nature of Mathematical Difficulty: Problems on the Edge of Possibility**

One of the most striking aspects of Tao’s thinking lies in his understanding of what makes a mathematical problem truly difficult. He argues that problems that are *impossibly hard*—such as the Riemann Hypothesis or the Twin Prime Conjecture—are not the most intellectually compelling. Instead, the most fascinating challenges exist on the boundary between solvable and unsolvable, where existing tools can resolve 90% of the issue, but the final 10% remains stubbornly out of reach.

Tao identifies the Kakeya problem as a seminal example of such a challenge. Originally posed by Japanese mathematician Soichi Kakeya in 1918, the problem asks: *What is the smallest area in the plane required to rotate a unit-length needle 180 degrees?* At first glance, one might assume the minimal area is a circle of radius 1/2 (area = π/4), or perhaps a three-point U-turn (area = π/8). However, in a groundbreaking result, Abram Besicovitch demonstrated that the needle could be rotated in *arbitrarily small area*—approaching zero.

This result, counterintuitive and deeply surprising, arises from a complex, back-and-forth motion that causes the needle to pass through every possible orientation. The construction relies on a fractal-like structure, where the needle is maneuvered through a series of increasingly narrow corridors, exploiting the fact that in two dimensions, area is not a barrier to rotation.

Tao extends this idea into three dimensions, posing a natural question: *What is the smallest volume required to rotate a thin, rigid tube (like a telescope) through all possible directions in space?* If the tube has zero thickness, the answer is again zero—by analogy to the 2D case. But for a tube of finite thickness δ, the minimal volume depends on δ. The conjecture is that this volume decreases only logarithmically with δ, a remarkably slow rate.

This problem is not merely a geometric curiosity. It has deep connections to partial differential equations (PDEs), particularly in wave propagation. When waves travel through a medium, they can focus into singularities—points of infinite amplitude—under certain conditions. The Kakeya problem helps determine whether such focusing is possible under realistic physical constraints.

For example, in fluid dynamics, wave energy can concentrate in a small region, potentially leading to a "blowup" in the solution of the Navier-Stokes equations. If the Kakeya conjecture were false—meaning energy could be packed into extremely narrow volumes—then such singularities might be more common than previously thought. Thus, the Kakeya problem serves as a critical test for the stability of physical models.

---

### **2. The Navier-Stokes Equations: A Century-Long Challenge**

The Navier-Stokes equations, which describe the motion of incompressible fluids like water, represent one of the most enduring mysteries in mathematical physics. The Clay Mathematics Institute has designated the regularity of solutions to these equations as one of its seven Millennium Prize Problems, offering a $1 million reward for a solution.

The central question is whether smooth initial conditions (e.g., a calm fluid) can evolve into a state of infinite velocity at a finite time—known as a "finite-time blowup." In physical reality, such a phenomenon does not occur. Water in a bathtub, for instance, eventually settles into a calm state, even if it initially exhibits turbulence.

Mathematically, however, the possibility remains open. The equations are nonlinear, meaning that small changes in initial conditions can lead to large, unpredictable outcomes. The balance between viscosity (which damps energy) and transport (which moves energy from one region to another) determines whether the solution remains smooth or blows up.

Tao’s approach to this problem was revolutionary. Rather than attempting to prove global regularity (i.e., that no blowup occurs), he constructed a *modified* version of the Navier-Stokes equations—specifically, an "averaged" version—where blowup *is* possible. This was not a proof of the original problem, but a *counterexample* to certain types of proof strategies.

The key insight was to engineer a system where energy is funneled from large-scale motions to increasingly smaller scales in a controlled, sequential manner. In the original equations, energy tends to spread out across many scales, making it vulnerable to damping by viscosity. But in Tao’s artificial model, energy is kept localized at a single scale at a time, like a wave that moves through a series of airlocks.

To achieve this, he designed a nonlinear system that mimics the behavior of electronic circuits. He used components analogous to resistors, capacitors, and logic gates, inspired by his wife’s background in electrical engineering. The system was structured so that energy would only be transferred to the next scale once the previous one was fully exhausted—a "delayed" transfer mechanism.

This construction was not a direct solution to the Navier-Stokes problem, but it demonstrated that any proof of regularity must rely on features *not present* in this artificial model. In effect, it ruled out a large class of potential proof techniques, showing that they would fail even in a simplified setting.

Tao’s work thus provides a *meta-level* understanding of the problem. It does not resolve the Navier-Stokes conjecture, but it reveals the *obstacles* that any future proof must overcome. This is a hallmark of deep mathematical insight: not just solving a problem, but understanding why it is so difficult.

---

### **3. The Role of Intuition, Structure, and Randomness**

Tao frequently reflects on the duality between structure and randomness in mathematics. He notes that most mathematical objects, when generated at random, appear to lack pattern. Yet, a few contain deep, hidden structure—such as the prime numbers, which, despite being generated by a simple rule (numbers not divisible by any smaller number), exhibit behavior that resembles randomness.

This duality is central to his work on the Green-Tao theorem, which proves that the prime numbers contain arithmetic progressions of any length. This was a major breakthrough because, while primes are sparse and irregular, they still contain long, structured sequences.

Tao explains that this is possible because arithmetic progressions are "indestructible"—they persist even if the primes are slightly altered. In contrast, the twin prime conjecture (that there are infinitely many pairs of primes differing by 2) is far more fragile. A small, carefully chosen modification to the prime sequence—removing just 0.01% of primes—can eliminate all twin primes while preserving all known statistical properties.

This fragility makes the twin prime conjecture significantly harder to prove. It suggests that any proof must rely on subtle, global features of the primes, not just statistical averages.

To address this, Tao and others have developed "inverse theorems" that identify when a set of numbers must be structured. These theorems state that if a function or sequence exhibits a certain kind of regularity, then it must be close to a structured object (e.g., a polynomial, a periodic function). This dichotomy—either a set is random, or it is structured—has become a powerful tool in modern number theory.

---

### **4. The Power of Abstraction: From Cellular Automata to Fluid Computation**

One of the most imaginative ideas in Tao’s work is the concept of a *fluid computer*. He proposes that if the Navier-Stokes equations could support computation—much like how electronic circuits process information—then it might be possible to construct a system that, when initialized with a specific configuration, evolves into a self-replicating structure that eventually causes a blowup.

This idea draws inspiration from Conway’s Game of Life, a cellular automaton where simple rules give rise to complex, self-sustaining patterns. In this system, "gliders" and "glider guns" can be built to perform logic operations. Tao suggests that a similar structure could emerge in a fluid, where vortices or pressure waves act as bits, and interactions between them perform logical operations.

Such a system would not be a literal computer, but a *mathematical model* of computation. If such a structure could be proven to exist within the Navier-Stokes equations, it would imply that blowup is not only possible but *inevitable* under certain initial conditions.

This idea is not meant to be taken literally as a physical device. Rather, it is a *thought experiment* to test the limits of mathematical models. It illustrates how deep mathematical problems can be reframed as questions about computation and information.

---

### **5. The Role of Collaboration and Formalization: The Rise of Lean**

Tao has become a leading advocate for formal proof systems, particularly the Lean theorem prover. Unlike traditional mathematical writing, which relies on human judgment, Lean produces *machine-verified* proofs—each step is checked by a computer, ensuring logical correctness.

Tao describes the experience of using Lean as akin to having a "pedantic colleague" who never makes mistakes but constantly asks for clarification. Every object must have a defined type (e.g., a real number, a function), and every assumption must be justified.

This rigor has profound implications. For example, when Tao and collaborators formalized a proof involving a constant (e.g., 12), they discovered that changing it to 11 required only a few lines of code to be modified—because the rest of the proof remained valid. This is impossible to verify by hand, but with Lean, the system immediately highlights the affected lines.

Tao sees this as a revolutionary shift. Formalization allows for *massive collaboration* on mathematical proofs, where dozens of researchers can work on separate parts of a proof simultaneously, with confidence that the whole remains consistent. This is a new model of mathematical research—one that resembles a modern software supply chain.

He envisions a future where mathematical research is not dominated by a few "geniuses," but by a global, distributed community of contributors, each responsible for a small, verifiable piece.

---

### **6. The Future of Mathematics: AI and the Human Mind**

Tao is deeply engaged with the rise of artificial intelligence in mathematics. He acknowledges that current language models, such as those used in AlphaProof, can generate plausible-sounding proofs of high school-level problems—such as those from the International Mathematical Olympiad (IMO). However, these models often fail due to subtle errors that are invisible to human readers.

The key challenge lies in *mathematical smell*—the intuitive sense that a proof approach is flawed, even if it appears correct. Humans develop this through experience, but AIs currently lack it. They can mimic correctness, but not true understanding.

Tao believes that the future of mathematics lies in *collaboration* between humans and AI. He imagines a future where a mathematician and an AI engage in a free-form dialogue: the human proposes a strategy, the AI evaluates it, suggests alternatives, and performs calculations. The AI might say, "I’ve checked 100 cases up to N=1000, and the pattern holds," or "There’s a counterexample at N=46."

This kind of interaction, he argues, would not replace human mathematicians, but would *amplify* their abilities. The human provides creativity, intuition, and vision; the AI provides speed, accuracy, and exhaustive checking.

He predicts that by 2026, AI-assisted research will be common in mathematics. By 2030, it may be standard for papers to be submitted in Lean format, with referees focusing on significance rather than correctness.

---

### **7. The Human Element: Humility, Persistence, and the Joy of Discovery**

Despite his extraordinary achievements, Tao remains deeply humble. He recalls a moment after winning the Fields Medal when someone asked him what he would do now. His response was simple: "The shiny metal won’t solve any of my problems. I’ll keep working."

This reflects a core belief: mathematical progress is not about awards, but about the intrinsic joy of solving problems. He admires figures like Grigori Perelman, who famously declined both the Fields Medal and the $1 million Millennium Prize, stating that the proof’s correctness was all that mattered.

Tao sees Perelman as a rare example of someone who prioritized truth over recognition. Yet he also recognizes that such a stance is not sustainable for most. The mathematical community, he notes, is a social institution. As one gains status, one gains responsibility—advising students, reviewing papers, shaping the field.

He emphasizes that mathematical talent is not a single trait but a spectrum. Some mathematicians are "hedgehogs"—deeply focused on one area. Others are "foxes"—broadly curious, drawing connections across fields. Tao identifies as a fox, but he respects both styles.

He also reflects on the emotional toll of mathematical research. There are moments when weeks of work are undone by a single missing term. But he has learned to step away, to switch problems, to avoid burnout.

---

### **8. The Ultimate Questions: What Is Mathematics?**

Tao concludes with a philosophical reflection on the nature of mathematics. He sees it not as a description of reality, but as a *model* of reality—built from axioms, tested against observations, and refined over time.

He draws a parallel between mathematical models and physical theories. Just as a physicist might use a "spherical cow" to simplify a problem, a mathematician uses idealized abstractions to explore structure.

The success of mathematics lies in its *unreasonable effectiveness*—the fact that abstract structures often describe the physical world with astonishing precision. This, Tao believes, is not a coincidence, but a sign that the human mind, through abstraction, can uncover deep truths about the universe.

---

### **Brief Outline of the Original Text**

1. **Introduction to Terence Tao** – Recognition of his status as a mathematical genius, his awards, and personal humility.
2. **The Kakeya Problem** – A deep dive into the geometric puzzle of rotating a needle in minimal area, its implications for wave propagation, and its connection to PDEs.
3. **Navier-Stokes and Blowup** – Tao’s construction of a modified Navier-Stokes equation that allows finite-time blowup, illustrating the difficulty of proving regularity.
4. **Structure vs. Randomness** – The role of mathematical structure in number theory, particularly in the Green-Tao and twin prime theorems.
5. **Fluid Computation and Self-Replication** – The speculative idea of a fluid-based Turing machine, inspired by cellular automata.
6. **Formal Proof and Lean** – The use of proof assistants to verify mathematical arguments, enabling large-scale collaboration.
7. **AI in Mathematics** – The potential and limitations of AI in proof generation, with a focus on AlphaProof and future possibilities.
8. **The Human Mind in Mathematics** – Reflections on intuition, collaboration, emotional resilience, and the role of humility.
9. **The Future of Mathematics** – A vision of a world where AI and human mathematicians co-create knowledge, with formalization enabling global, distributed research.
10. **Final Reflections** – On the nature of mathematical truth, the beauty of abstraction, and the enduring mystery of prime numbers.

---

**Final Summary (in English):**

This detailed paraphrase of a conversation with Terence Tao explores the depth, breadth, and philosophical underpinnings of modern mathematical thought. It examines how Tao approaches difficult problems by identifying the boundary between solvable and unsolvable, using tools from geometry, analysis, and computation. His work on the Kakeya and Navier-Stokes problems illustrates how mathematical insight often comes not from direct solution, but from constructing counterexamples that reveal the limits of existing methods.

The discussion extends to the role of structure and randomness in number theory, the potential for fluid systems to perform computation, and the transformative impact of formal proof systems like Lean. Tao envisions a future where mathematics becomes a collaborative, distributed enterprise, powered by AI and open to global participation.

Ultimately, the text portrays mathematics not as a static body of knowledge, but as a living, evolving process of discovery—driven by curiosity, creativity, and the enduring human desire to understand the universe through the language of logic and pattern.