---
layout: post
title: "475 - Demis Hassabis: Future of AI, Simulating Reality, Physics and Video Games"
date: 2025-07-23 09:00:00 +0000
article_id: 475-demis-hassabis-future-of-ai-simulating-reality-physics-and-video-games
article_title: "475 - Demis Hassabis: Future of AI, Simulating Reality, Physics and Video Games"
collection_id: lex-fridman
language: en
variant_rank: 1
original_link: "https://www.youtube.com/watch?v=-HzgcbRXUK8"
excerpt: "In this episode, Demis Hassabis discusses AI's ability to model complex systems like fluid dynamics, suggesting models such as Veo learn physical structures implicitly rather than through programming. He explores how nature's inherent constraints create learnable patterns, raising questions about computation and the limits of modeling reality."
permalink: /articles/475-demis-hassabis-future-of-ai-simulating-reality-physics-and-video-games/en/
---


### **The Nature of Reality, Intelligence, and the Limits of Computation**

The human mind struggles to make clean, deterministic predictions about complex, nonlinear dynamical systems—systems that evolve over time in ways that are sensitive to initial conditions, often exhibiting chaotic behavior. Yet, despite this inherent difficulty, there is growing evidence that classical machine learning systems, particularly deep neural networks, may be capable of modeling such systems with surprising accuracy. This includes domains long considered intractable, such as fluid dynamics.

Fluids, governed by the Navier-Stokes equations, represent a class of problems that have historically demanded massive computational resources. Weather prediction systems, for example, rely on solving these equations numerically across vast spatial and temporal scales. These simulations require supercomputers and days of processing time. And yet, models like **Veo**, Google DeepMind’s video generation system, demonstrate an uncanny ability to simulate liquids, materials, and even complex lighting phenomena such as specular reflections—features that are central to the physical world.

These capabilities are not merely aesthetic flourishes. The fact that Veo can generate videos of clear liquids being compressed through hydraulic presses, with realistic fluid behavior and material deformation, suggests something profound: the model is not just memorizing patterns from training data, but extracting and internalizing the underlying physical structure of how materials behave.

This observation leads to a deeper hypothesis: **if natural systems—biological, physical, geological, even cosmological—have evolved under selective pressures over time, they may possess an inherent structure or "manifold" that is learnable by artificial systems.** This structure is not random; it emerges from processes of survival, stability, and optimization. As such, it may be possible to reverse-engineer these patterns through observation alone—without explicit programming of physical laws.

Demis Hassabis, in conversation, reflects on his early career in game development, where he wrote physics engines and graphics systems from scratch. He recalls how painstakingly difficult it was to code even basic fluid behavior, let alone complex interactions like liquid compression or material fracture. Yet today’s AI models, trained only on video data from YouTube, appear to have learned these dynamics implicitly—by observing how liquids behave in the wild.

This raises a fundamental question: **what is it about nature that makes it amenable to efficient modeling by classical computing systems?** The answer, according to Hassabis, lies in the fact that nature is not random. It is shaped by evolutionary, thermodynamic, and physical constraints. These constraints create a low-dimensional manifold within the high-dimensional space of possible configurations. Neural networks, by nature, are excellent at identifying and navigating such manifolds.

Thus, the conjecture he proposes—though framed provocatively—is that **any pattern found in nature, if it has evolved or been shaped by selection, can be efficiently discovered and modeled by classical learning algorithms.** This includes systems in biology, chemistry, physics, neuroscience, and even cosmology.

---

### **The Conjecture: Learnability of Natural Systems**

This idea is not merely speculative. It is grounded in the success of projects like **AlphaGo**, **AlphaFold**, and **AlphaGenome**, which have solved problems previously considered computationally intractable.

- **AlphaGo** defeated world champions in Go, a game with more possible positions than atoms in the universe. The solution was not brute-force search, but a learned model of the game’s dynamics, combined with a search algorithm (Monte Carlo Tree Search) that guided the process toward high-value moves.
- **AlphaFold** solved the protein folding problem—predicting 3D structures from amino acid sequences—by modeling the energy landscape of proteins and learning the relationships between sequence and structure.
- **AlphaFold 3** extends this to interactions between proteins, RNA, and DNA, capturing complex biological networks.
- **AlphaGenome** predicts how small genetic mutations affect protein function, bridging the gap between genotype and phenotype.

These systems do not brute-force through all possibilities. Instead, they model the environment—the "dynamics of the system"—and use that model to guide search and prediction. This approach mirrors how nature itself solves problems: proteins fold in milliseconds because they follow energy gradients, not because they explore every possible conformation.

Hassabis argues that this success suggests a broader principle: **if a system has structure due to evolutionary or physical selection, it is likely learnable.** The key insight is that **the universe is not a random search space. It is shaped by constraints—physical laws, evolutionary pressures, thermodynamic limits—that create a kind of "landscape" that is navigable.**

This leads to a proposed new complexity class: **LNS (Learnable Natural Systems)**. This would represent a subset of problems that, while potentially NP-hard, are not intractable because they possess structure that can be exploited by classical learning systems.

He draws a parallel to the P vs. NP problem: if P = NP, then every problem whose solution can be verified quickly can also be solved quickly. But if nature can solve such problems efficiently, and if we can replicate that process, then perhaps P = NP is not just a mathematical conjecture, but a physical one—rooted in the structure of reality.

---

### **The Universe as an Informational System**

Hassabis posits a radical view: **the universe is fundamentally informational.** He argues that information is more fundamental than matter or energy. All physical processes, he suggests, can be reduced to transformations of information. This perspective reframes the P vs. NP question not as a purely mathematical puzzle, but as a **physics question**—one about the limits of computation in a universe governed by information.

From this vantage point, the success of neural networks in modeling complex systems is not a coincidence. It suggests that **the universe is structured in a way that is compatible with classical computation.** The fact that a model like Veo can simulate fluid dynamics, lighting, and material behavior—without being explicitly trained on the Navier-Stokes equations—implies that it has learned the **intuitive physics** of the world.

This "intuitive physics" is not symbolic or rule-based. It is not a set of equations. It is a **latent understanding of how objects behave under forces, how liquids flow, how light reflects off surfaces.** This is akin to how a human child learns physics through experience, not through formal education.

This challenges long-held assumptions in AI: that understanding the world requires **embodied experience**—interaction with the physical world through a robot body. But Veo, which has never touched a liquid, nor interacted with a physical environment, still generates videos that are nearly indistinguishable from real footage.

This suggests that **passive observation alone may be sufficient to learn the dynamics of reality.** The model is not simulating physics from scratch. It is learning the statistical regularities of how the world behaves, and using that to generate coherent, temporally consistent sequences.

---

### **The Role of Intuition and Creativity in AI**

This leads to a deeper philosophical question: **what does it mean to "understand" something?**

Hassabis acknowledges that current models do not possess human-like understanding. They do not have beliefs, desires, or self-awareness. But they do exhibit a form of understanding: **the ability to predict the next frame in a video with high coherence.**

He defines understanding as **predictive accuracy within a structured, dynamic environment.** If a model can generate eight seconds of video that, at a glance, are hard to distinguish from real footage—especially when it comes to complex phenomena like fluid flow, material deformation, or lighting—then it must have captured some essential aspects of physical reality.

This raises the possibility that **AI systems are developing a kind of "intuitive physics"**—a non-symbolic, implicit grasp of how the world works. This is not the same as human intuition, but it is a functional approximation.

He draws a distinction between **symbolic reasoning** (e.g., solving a math problem with formal logic) and **intuitive reasoning** (e.g., knowing that if you push a glass off a table, it will fall and break). The latter is what AI is beginning to emulate.

This has profound implications for creativity. The most difficult part of scientific discovery is not solving a problem, but **formulating the right question.** This is what Hassabis calls "research taste"—the ability to identify a hypothesis that is both novel and falsifiable, that lies at the "sweet spot" between being too easy and too hard.

Current AI systems cannot do this. They can solve problems, but they cannot invent new ones. They cannot propose a conjecture worthy of a mathematician like Terence Tao. This remains one of the hardest challenges in AI.

But he suggests that **this may not be a fundamental barrier.** If we can design systems that combine:
- **Foundation models** (like LLMs or diffusion models),
- **Search algorithms** (like Monte Carlo Tree Search or evolutionary algorithms),
- **Objective functions** (to guide optimization),

then we may be able to create systems that **discover new hypotheses, new laws, new structures**—just as evolution discovered life, or as Einstein discovered relativity.

---

### **The Evolution of Intelligence: From AlphaGo to AGI**

The journey from AlphaGo to AGI is not a linear progression. It is a series of **"move 37" moments**—unexpected, creative breakthroughs that change the game.

- In **AlphaGo**, move 37 was a move that no human player had ever made. It was not based on any known opening or pattern. It was a leap of intuition, later proven to be optimal.
- In **AlphaFold**, the breakthrough was not a single move, but a **new architecture** that modeled protein folding as a probabilistic energy landscape, rather than a deterministic structure.

These were not just improvements. They were **creative leaps**—the kind that require not just more data or compute, but a new way of thinking.

Hassabis suggests that **future AGI systems may not emerge from a single breakthrough, but from a combination of incremental progress and rare, transformative insights.** The path to AGI may resemble a series of **S-curves**, where progress is steady for a while, then accelerates due to a new idea.

He notes that **scaling laws**—the relationship between model size, data, and compute—are still holding. But he warns that **scaling alone may not be enough.** We may need one or two more "big leaps" in architecture, search, or learning theory.

One promising direction is **hybrid systems**, such as **AlphaEvolve**, which combines:
- **Large Language Models (LLMs)** to propose new program designs,
- **Evolutionary algorithms** to explore and optimize those designs.

This is not just a technical trick. It reflects a deeper truth: **evolution is a powerful search algorithm.** It does not rely on a single optimal path. It explores the space of possibilities through mutation, recombination, and selection.

AlphaEvolve demonstrates that **evolutionary search, when guided by a foundation model, can discover novel algorithms—such as faster matrix multiplication—without human intervention.**

This suggests that **the same mechanisms that created life over billions of years might be harnessed to create artificial intelligence.** The key insight is that **evolution is not just about survival. It is about building complexity.** It combines simple parts into new, functional wholes.

---

### **The Dream of a Virtual Cell**

One of Hassabis’s most ambitious long-term goals is to **simulate a living cell in silico**—a "virtual cell" that can be used to run experiments, predict outcomes, and accelerate biological discovery.

This is not a fantasy. It is a **step-by-step project**, built on prior successes:
- **AlphaFold** solved the static 3D structure of proteins.
- **AlphaFold 3** models interactions between proteins, RNA, and DNA.
- **AlphaGenome** predicts how genetic mutations affect function.

The next step is to **model the dynamics of these interactions over time.** This includes:
- **Temporal scaling**: Some processes (like protein folding) happen in nanoseconds; others (like cell division) take hours.
- **Hierarchical modeling**: Different subsystems operate at different time scales. A model must be able to jump between them.
- **Emergent behavior**: The cell is more than the sum of its parts. Its function emerges from complex, nonlinear interactions.

Hassabis suggests starting with a **yeast cell**, which is a single-celled organism and a well-studied model system. The goal is not to replicate every atom, but to **capture the essential dynamics at the protein level**, using AlphaFold as a foundation.

This would allow researchers to:
- Run thousands of virtual experiments,
- Predict how a drug will affect a cell,
- Simulate disease progression,
- Reduce reliance on wet lab experiments by 100x.

The ultimate dream is not just to simulate a cell, but to **simulate the origin of life**—to model how non-living chemicals could have self-organized into a living system.

This would require simulating:
- **Primordial soup** (a mixture of amino acids, nucleotides, lipids),
- **Environmental conditions** (hydrothermal vents, temperature, pH),
- **Self-replication** and **metabolism**.

This is not just a scientific goal. It is a **philosophical one.** It challenges the traditional boundary between "living" and "non-living." Hassabis believes that **life is not a binary state, but a continuum.** The transition from chemistry to biology may be gradual, not abrupt.

If we can simulate this process, we may finally answer one of the deepest questions: **What is life?**

---

### **The Future of Video Games and Interactive Worlds**

Hassabis reflects on his deep personal connection to video games—his first love, his first professional work, and a lifelong passion.

He recalls working on **Theme Park**, **Black & White**, and other open-world games where players co-create the experience. These games were not linear. They were **simulations**, with AI characters that evolved based on player behavior.

Today, he sees a future where **AI-generated worlds are not just simulated, but interactive.** Imagine a game where:
- The world is generated on the fly based on your choices,
- NPCs have beliefs, emotions, and long-term goals,
- The story adapts to your actions in real time,
- You can step into the world and explore it freely.

This is not science fiction. It is a **logical extension of systems like Veo.** If a model can generate eight seconds of coherent video, it can generate **eight hours, eight days, or eight years** of video—provided the model is stable and the search process is guided.

He envisions a future where **interactive video games become "world models"**—dynamic, persistent simulations of reality. These would not be games in the traditional sense, but **digital universes** where users can explore, experiment, and even live.

This would represent a **new form of human experience**—one that blends creativity, exploration, and social interaction in ways that no other medium can.

---

### **The Path to AGI: Signs of a True General Intelligence**

Hassabis estimates a **50% chance of AGI by 2030**, but he cautions that the definition matters.

He defines AGI as a system that:
- Matches the full range of human cognitive abilities,
- Is consistent across domains (not jagged),
- Can invent new hypotheses, games, or theories,
- Can explain its reasoning clearly.

He suggests that **AGI will not be recognized by a single benchmark**, but by **"move 37" moments**—unexpected, creative breakthroughs.

Examples of such moments:
- **Inventing a new scientific theory**, like Einstein’s relativity.
- **Creating a game as deep and beautiful as Go**, not just a new strategy, but a new form of play.
- **Solving a problem that has resisted human thought for centuries.**

He imagines a scenario where such a system is tested against the best human minds—mathematicians, physicists, artists. If they cannot find a flaw, then we may have reached AGI.

He also acknowledges that **humans may miss such breakthroughs**, just as a chess grandmaster might not immediately understand a brilliant move. But if the system can **explain its reasoning**, and if the explanation is **coherent and elegant**, then we may accept it.

---

### **The Role of Human Collaboration and Ethics**

Despite the competitive nature of AI, Hassabis emphasizes **collaboration**. He maintains good relationships with leaders at other labs, including Elon Musk.

He believes that **the most important challenge is not technical, but ethical.** AGI is a **dual-use technology**—it could cure all diseases, end energy scarcity, and enable space colonization. But it could also be misused.

He warns that **bad actors could repurpose AI for harm**, and that **guardrails must be built in from the start.**

He supports **international cooperation**, such as a **CERN-style collaboration**, to ensure that AGI is developed responsibly.

He also believes that **AI should not replace human creativity**, but **amplify it.** The future is not one where humans are replaced, but where they **work with AI to achieve more than either could alone.**

---

### **Conclusion: The Human Condition in the Age of AI**

Hassabis ends with a note of hope. He believes in the **infinite potential of human ingenuity, adaptability, and compassion.**

He sees AI not as a threat, but as a **tool to help us solve the greatest mysteries of existence**—the nature of consciousness, the origin of life, the structure of reality.

He quotes Feynman: *"What I cannot create, I do not understand."* He sees AI as a way to **test and expand our understanding**—not just of the world, but of ourselves.

And he believes that **the most profound questions are not about technology, but about meaning.** What does it mean to be human? What is consciousness? What is life?

These are not just scientific questions. They are **spiritual, philosophical, and deeply human.**

And in the end, he says, **the most important thing is not to build a smarter machine, but to become wiser humans.**

---

### **Brief Outline of the Text**

1. **Introduction to the Challenge of Nonlinear Systems**  
   - Humans struggle to predict complex, dynamic systems.  
   - AI models like Veo demonstrate surprising ability to simulate fluid dynamics and materials.

2. **The Learnability Conjecture**  
   - Natural systems are structured due to evolutionary and physical constraints.  
   - This structure may be learnable by classical systems.  
   - Proposal of a new complexity class: **LNS (Learnable Natural Systems)**.

3. **The Universe as an Informational System**  
   - Information is more fundamental than matter or energy.  
   - P vs. NP may be a physical question, not just mathematical.

4. **Intuitive Physics in AI**  
   - Models like Veo learn "intuitive physics" through observation.  
   - This challenges the need for embodied experience in learning.

5. **Creativity and Research Taste**  
   - The hardest part of science is not solving problems, but asking the right questions.  
   - Current AI cannot invent new hypotheses, but may in the future.

6. **Evolution as a Search Algorithm**  
   - AlphaEvolve combines LLMs and evolutionary search.  
   - Evolution is powerful because it builds complexity through recombination.

7. **The Virtual Cell Project**  
   - Long-term goal: simulate a living cell.  
   - Building on AlphaFold, AlphaFold 3, and AlphaGenome.  
   - Challenges: temporal scaling, emergent behavior, hierarchical modeling.

8. **The Origin of Life Simulation**  
   - Goal: model how non-living chemistry gave rise to life.  
   - A continuum, not a binary, between living and non-living.

9. **The Future of Interactive Worlds**  
   - Video games evolve into persistent, AI-generated "world models."  
   - Players co-create experiences in real time.

10. **Signs of AGI**  
   - Not a single benchmark, but "move 37" moments:  
     - Inventing a new theory.  
     - Creating a game as deep as Go.  
   - Must be explainable and consistent.

11. **Ethics and Collaboration**  
   - AGI is dual-use.  
   - Need for international cooperation, like CERN.  
   - Humans and AI must work together.

12. **Final Reflections**  
   - Hope lies in human ingenuity, adaptability, and compassion.  
   - AI is a tool to help us understand reality—and ourselves.
