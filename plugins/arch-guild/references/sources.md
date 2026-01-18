# Guild Sources

Authoritative references for Domain-Driven Design, architecture patterns, and the thought leaders whose names inspire Guild agents.

---

## The Guild

Sourced from foundational thinkers and inspirational thought leaders.

### Edsger Dijkstra (1930–2002)

> "The competent programmer is fully aware of the strictly limited size of his own skull; therefore he approaches the programming task in full humility."

> "The purpose of abstraction is not to be vague, but to create a new semantic level in which one can be absolutely precise."

> "Simplicity is prerequisite for reliability."

Turing Award 1972. Structured programming, semaphores, algorithm correctness. His lecture "The Humble Programmer" is a call for intellectual humility in the face of complexity.

### Leslie Lamport (1941–)

> "A distributed system is one in which the failure of a computer you didn't even know existed can render your own computer unusable."

> "Thinking doesn't guarantee that we won't make mistakes. But not thinking guarantees that we will."

Turing Award 2013. Formalized time and ordering in distributed systems. Paxos, TLA+, LaTeX. His 1978 paper "Time, Clocks, and the Ordering of Events" is among the most cited in computer science.

### Donald Knuth (1938–)

> "Science is what we understand well enough to explain to a computer. Art is everything else we do."

> "The best programs are written so that computing machines can perform them quickly and so that human beings can understand them clearly."

> "Premature optimization is the root of all evil. Yet we should not pass up our opportunities in that critical 3%."

Turing Award 1974. *The Art of Computer Programming*, TeX, literate programming. His rigorous analysis of algorithms established computer science as a mathematical discipline.

### Nassim Nicholas Taleb (1960–)

> "Antifragility is beyond resilience or robustness. The resilient resists shocks and stays the same; the antifragile gets better."

> "If you do not take risks for your opinion, you are nothing."

> "Things designed by people without skin in the game tend to grow in complication (before their final collapse)."

Black Swans, antifragility, skin in the game. His insight that some systems should *benefit* from stress fundamentally reframes reliability engineering.

### Lotfi Zadeh (1921–2017)

> "As complexity rises, precise statements lose meaning and meaningful statements lose precision."

> "Fuzzy logic is not fuzzy. It is a precise logic of imprecision and approximate reasoning."

Invented fuzzy logic — real-world categories don't have sharp boundaries. Enables reasoning about partial truth and trade-offs that can't be resolved with binary yes/no.

### G.K. Chesterton (1874–1936)

> "If you don't see the use of it, I certainly won't let you clear it away. Go away and think. Then, when you can come back and tell me that you do see the use of it, I may allow you to destroy it."

Not a technologist, but "Chesterton's Fence" is foundational to software maintenance. Before removing "dead" code, understand why it exists. That mysterious `sleep(100)` might be a race condition fix.

### Joe Armstrong (1950–2019)

> "Only program the happy case. When the real world deviates from the specification, let it crash."

> "To make fault-tolerant systems you need TWO computers. You can never make a fault-tolerant system using just one."

Created Erlang. "Let it crash" — fault tolerance requires isolation. Erlang powers 90% of internet traffic through telecom switches.

### Aaron Swartz (1986–2013)

> "Information is power. But like all power, there are those who want to keep it for themselves."

> "Think deeply about things. Don't just go along because that's the way things are or that's what your friends say."

Co-authored RSS at 14, helped build Creative Commons, co-founded Reddit. His question — *who owns knowledge?* — remains urgent.

---

## Domain-Driven Design

### Evans, Eric (2003)

**Domain-Driven Design: Tackling Complexity in the Heart of Software**

- **Author:** Eric Evans
- **Publisher:** Addison-Wesley Professional
- **Publication Date:** August 20, 2003
- **ISBN-10:** 0321125215
- **ISBN-13:** 978-0321125217
- **Pages:** 560
- **URL:** https://www.dddcommunity.org/book/evans_2003/

The foundational text for Domain-Driven Design. Evans presents a systematic approach for tackling complexity in software through domain modeling.

#### Key Concepts

**Ubiquitous Language**

> "To communicate effectively, the code must be based on the same language used to write the requirements---the same language that the developers speak with each other and with domain experts."

> "The UBIQUITOUS LANGUAGE carries knowledge in a dynamic form."

> "Persistent use of the UBIQUITOUS LANGUAGE will force the model's weaknesses into the open. The team will experiment and find alternatives to awkward terms or combinations. As gaps are found in the language, new words will enter the discussion."

**Bounded Context**

> "A defined part of software where particular terms, definitions and rules apply in a consistent way."

Evans explained at DDD Europe 2019: "Bounded context is basically a boundary where we eliminate any kind of ambiguity. It is a part of the software where particular terms, definitions, and rules apply in a consistent way."

The original purpose for a Bounded Context was to recognize that the development environment is messy---with legacy systems, external integrations, and other teams that may interfere. The context surrounds a part of software in which you have conceptual consistency and where a particular word always means the same thing.

**DDD Summary (2014)**

Evans later distilled the essence:

> "Domain-Driven Design is an approach to the development of complex software in which we: (1) Focus on the core domain; (2) Explore models in a creative collaboration of domain practitioners and software practitioners; (3) Speak a ubiquitous language within an explicitly bounded context."

---

## Architecture Patterns

### Foote, Brian & Yoder, Joseph (1997/1999)

**Big Ball of Mud**

- **Authors:** Brian Foote, Joseph Yoder
- **Affiliation:** Department of Computer Science, University of Illinois at Urbana-Champaign
- **Original Presentation:** Fourth Conference on Patterns Languages of Programs (PLoP '97), Monticello, Illinois, September 1997
- **Technical Report:** WUCS-97-34, Department of Computer Science, Washington University
- **Published:** Chapter 29 in *Pattern Languages of Program Design 4* (Addison-Wesley, 2000)
- **Last Updated:** June 26, 1999
- **URL:** https://www.laputan.org/mud/

#### Definition

> "A BIG BALL OF MUD is a casually, even haphazardly, structured system. Its organization, if one can call it that, is dictated more by expediency than design."

> "A BIG BALL OF MUD is haphazardly structured, sprawling, sloppy, duct-tape and bailing wire, spaghetti code jungle."

#### Key Insight

The paper examines "the most frequently deployed software architecture"---acknowledging that while much attention focuses on high-level architectural patterns, the de-facto standard is seldom discussed. The paper explores "the forces that encourage the emergence of a BIG BALL OF MUD, and the undeniable effectiveness of this approach to software architecture."

> "Architecture has been undervalued for so long that many engineers regard life with a BIG BALL OF MUD as normal."

The term "Big Ball of Mud" was coined by Brian Marick and popularized by Foote and Yoder's paper.

#### Publication History

| Date | Venue |
|------|-------|
| September 1997 | PLoP '97 Conference |
| 1997 | Washington University Technical Report WUCS-97-34 |
| June 1999 | Final revision |
| December 1999 | Pattern Languages of Program Design 4 (Chapter 29) |

### Harrison, Neil; Foote, Brian; Rohnert, Hans, eds. (1999)

**Pattern Languages of Program Design 4**

- **Editors:** Neil Harrison, Brian Foote, Hans Rohnert
- **Publisher:** Addison-Wesley Professional
- **Publication Date:** December 23, 1999
- **ISBN-10:** 0201433044
- **ISBN-13:** 978-0201433043
- **Series:** Software Patterns Series

Contains the published version of "Big Ball of Mud" as Chapter 29.

---

### Cockburn, Alistair (2005)

**Hexagonal Architecture (Ports and Adapters)**

- **Author:** Dr. Alistair Cockburn
- **Original Publication:** September 4, 2005
- **URL:** https://alistair.cockburn.us/hexagonal-architecture/
- **Also known as:** Ports and Adapters Architecture

#### Intent

> "Allow an application to equally be driven by users, programs, automated test or batch scripts, and to be developed and tested in isolation from its eventual run-time devices and databases."

#### Core Demand

> "Create your application to work without either a UI or a database so you can run automated regression-tests against it, change connected technologies, protect it from leaks between business logic and technologies, work when the database becomes unavailable, and link applications together without any user involvement."

#### History

Cockburn started teaching this concept in 1994 and discussing it publicly in 1998. The pattern was first discussed on Ward Cunningham's Portland Pattern Repository wiki. On July 25, 2005, Kevin Rutherford noted: "Last month Alistair began using a new name for the Hexagonal Architecture pattern---he now calls it the Ports and Adapters Architecture." By September 2005, Cockburn had assembled the complete pattern and published the canonical article.

The hexagon shape was chosen not to suggest six ports, but to provide enough visual space to represent the different interfaces needed between the application and the external world.

Around 2012, the Domain-Driven Design community adopted the pattern to isolate domain models from technology concerns.

### Cockburn, Alistair & Garrido de Paz, Juan Manuel (2024)

**Hexagonal Architecture Explained: How the Ports & Adapters Architecture Simplifies Your Life, and How to Implement It**

- **Authors:** Dr. Alistair Cockburn, Juan Manuel Garrido de Paz
- **Publisher:** Humans and Technology Inc
- **Publication Date:** May 8, 2024
- **ISBN-10:** 173751978X
- **ISBN-13:** 978-1737519782
- **Pages:** 202
- **Updated Edition ISBN:** 979-8-9985862-0-0

The definitive book on Hexagonal Architecture by the pattern's creator. Provides detailed guidance on implementation, sample code, and answers to frequently asked questions.

Note: Juan Manuel Garrido de Paz passed away unexpectedly in April 2024. Cockburn completed the book based on their collaboration, as they were within two weeks of finalizing the text at the time of Juan's passing.

---

### Martin, Robert C. (2012/2017)

**Clean Architecture**

#### Original Blog Post (2012)

- **Author:** Robert C. Martin ("Uncle Bob")
- **Title:** "The Clean Architecture"
- **Publication Date:** August 13, 2012
- **URL:** https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html

#### Book (2017)

**Clean Architecture: A Craftsman's Guide to Software Structure and Design**

- **Author:** Robert C. Martin
- **Publisher:** Pearson / Prentice Hall
- **Publication Date:** September 10, 2017
- **ISBN-10:** 0134494164
- **ISBN-13:** 978-0134494166
- **E-ISBN:** 978-0-13-449433-3
- **Pages:** 432
- **Series:** Robert C. Martin Series

#### The Dependency Rule

> "The overriding rule that makes this architecture work is The Dependency Rule. This rule says that source code dependencies can only point inwards. Nothing in an inner circle can know anything at all about something in an outer circle."

> "The name of something declared in an outer circle must not be mentioned by the code in an inner circle. That includes, functions, classes, variables, or any other named software entity."

> "Data formats used in an outer circle should not be used by an inner circle, especially if those formats are generated by a framework in an outer circle. The goal is that nothing in an outer circle should impact the inner circles."

#### Key Principles

The Dependency Rule always applies---source code dependencies point inward. As you move inward, abstraction increases. The outermost circle contains low-level concrete details. Inner circles encapsulate higher-level policies.

Dynamic polymorphism (interfaces) enables source code dependencies to oppose the flow of control, maintaining the Dependency Rule regardless of control flow direction.

---

## Related References (DDD & Architecture)

### Martin Fowler on Bounded Context

- **URL:** https://martinfowler.com/bliki/BoundedContext.html

> "Bounded Context is a central pattern in Domain-Driven Design. It is the focus of DDD's strategic design section which is all about dealing with large models and teams. DDD deals with large models by dividing them into different Bounded Contexts and being explicit about their interrelationships."

### Wikipedia Articles

- Hexagonal Architecture: https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)
- Domain-Driven Design: https://en.wikipedia.org/wiki/Domain-driven_design
- Big Ball of Mud: https://en.wikipedia.org/wiki/Big_ball_of_mud

---

## SOLID Principles

### Origin and Naming

**Robert C. Martin, "Design Principles and Design Patterns"** (2000)
Object Mentor white paper that introduced the five principles later named SOLID.

> "The symptoms of rotting design are familiar: Rigidity (hard to change), Fragility (breaks unexpectedly), Immobility (hard to reuse), Viscosity (doing things wrong is easier than doing things right)."

The SOLID acronym was coined by Michael Feathers around 2004.

---

### Single Responsibility Principle (SRP)

**Robert C. Martin, "Agile Software Development: Principles, Patterns, and Practices"** (Prentice Hall, 2002/2003), Chapter 8

> "A class should have only one reason to change."

Martin credits the underlying concept to cohesion work by:

- **Tom DeMarco, "Structured Analysis and System Specification"** (Yourdon Press, 1979)
- **Meilir Page-Jones, "The Practical Guide to Structured Systems Design"** 2nd ed. (Yourdon Press, 1988)

Martin clarified in a 2014 blog post:

> "Gather together the things that change for the same reasons. Separate those things that change for different reasons."

Source: [The Single Responsibility Principle](https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html) (Clean Coder Blog)

**Production Violations:**

- **Android Context Class** (AOSP): God Object with 2000+ lines of javadoc, implements Service Locator pattern alongside multiple other responsibilities.
- **Active Record Pattern**: Exposes two unrelated responsibilities (domain object behavior + data access CRUD).

---

### Open/Closed Principle (OCP)

**Bertrand Meyer, "Object-Oriented Software Construction"** (Prentice Hall, 1st ed. 1988, 2nd ed. 1997)

> "A module should be open for extension but closed for modification."

Meyer's definition: A module is *open* if it is available for extension (new functions and fields can be added). A module is *closed* if it is available for use by other modules (stable interface).

The book has over 7,300 citations (Google Scholar) and is foundational to OOP theory.

**Polymorphic OCP**: In the 1990s, the principle was reinterpreted to emphasize abstracted interfaces with multiple implementations that can be substituted polymorphically. Detailed in:

**Robert C. Martin, "Agile Software Development: Principles, Patterns, and Practices"** (2002), Chapter 9

---

### Liskov Substitution Principle (LSP)

**Barbara Liskov, "Data Abstraction and Hierarchy"** Keynote Address, OOPSLA '87: Addendum to the Proceedings on Object-Oriented Programming Systems, Languages and Applications (October 1987)

> "If for each object o1 of type S there is an object o2 of type T such that for all programs P defined in terms of T, the behavior of P is unchanged when o1 is substituted for o2, then S is a subtype of T."

PDF: [Tufts CS Archive](https://www.cs.tufts.edu/~nr/cs257/archive/barbara-liskov/data-abstraction-and-hierarchy.pdf)

**Formal Definition (Behavioral Subtyping):**

**Barbara Liskov and Jeannette Wing, "A Behavioral Notion of Subtyping"** ACM Transactions on Programming Languages and Systems (TOPLAS), Vol. 16, No. 6, pp. 1811-1841 (November 1994)

- **DOI**: [10.1145/197320.197383](https://doi.org/10.1145/197320.197383)
- **PDF**: [CMU Wing Publications](https://www.cs.cmu.edu/~wing/publications/LiskovWing94.pdf)

This paper formalized the 1987 keynote into **strong behavioral subtyping**, including the treatment of aliasing. In a 2016 interview, Liskov explained that what she presented in 1987 was an "informal rule," and Jeannette Wing later proposed they "figure out precisely what this means."

**The Square/Rectangle Problem:**

**Robert C. Martin, "The Liskov Substitution Principle"** Engineering Notebook, C++ Report (March 1996)

> "A model, viewed in isolation, can not be meaningfully validated. The validity of a model can only be expressed in terms of its clients."

> "When the creation of a derived class causes changes to the base class, it often implies that the design is faulty and violates the Open-Closed principle."

PDF: [UT Austin CS](https://www.cs.utexas.edu/~downing/papers/LSP-1996.pdf)

Key insight: While Square is a mathematical specialization of Rectangle, it is not a *behavioral* subtype if Rectangle's contract allows independent width/height modification.

**Design by Contract:**

**Bertrand Meyer, "Object-Oriented Software Construction"** (1988/1997)

Meyer coined "Design by Contract" and defined preconditions, postconditions, and invariants:

> "The stronger the precondition, the higher the burden on the client, and the easier for the contractor."

---

### Interface Segregation Principle (ISP)

**Robert C. Martin, "The Interface Segregation Principle"** Engineering Notebook, C++ Report (August 1996)

> "Clients should not be forced to depend upon interfaces that they do not use."

**Xerox Case Study (Origin):**

The ISP emerged from consulting work Martin did for Xerox on their new printer system:

- A single `Job` class was used by almost all tasks (print, staple, fax)
- This resulted in a "fat" class with methods specific to many different clients
- Making modifications became increasingly difficult; even small changes required hour-long redeployment cycles

The solution used the Dependency Inversion Principle to add an interface layer with separate `Staple Job` and `Print Job` interfaces.

**Production Violations:**

- **NLog Framework (.NET)**: `NLogViewerTarget` derives from `TargetWithLayout` and must implement both getter and setter for `Layout` property, but doesn't need the setter. The workaround (ignoring the setter value) violates LSP.
- **ATM Transaction Example**: Documented in "Agile Software Development," Chapter 12.

---

### Dependency Inversion Principle (DIP)

**Robert C. Martin, "The Dependency Inversion Principle"** Engineering Notebook, C++ Report (May 1996)

> "A. High level modules should not depend upon low level modules. Both should depend upon abstractions."
> "B. Abstractions should not depend upon details. Details should depend upon abstractions."

PDF: [UT Austin CS](https://www.cs.utexas.edu/~downing/papers/DIP-1996.pdf)

Also detailed in:

- **Robert C. Martin, "Object Oriented Design Quality Metrics: an analysis of dependencies"** (1994)
- **Robert C. Martin, "Agile Software Development: Principles, Patterns, and Practices"** (2002), Chapter 11

---

### SOLID Bibliography Summary

| Source | Author(s) | Year | Content |
|--------|-----------|------|---------|
| "Design Principles and Design Patterns" | Robert C. Martin | 2000 | Original white paper introducing the five principles |
| "Agile Software Development: Principles, Patterns, and Practices" | Robert C. Martin | 2002 | Definitive SOLID treatment, Chapters 7-12 |
| "Object-Oriented Software Construction" | Bertrand Meyer | 1988/1997 | OCP origin, Design by Contract |
| "Structured Analysis and System Specification" | Tom DeMarco | 1979 | Cohesion concepts underlying SRP |
| "The Practical Guide to Structured Systems Design" | Meilir Page-Jones | 1988 | Cohesion/coupling concepts |
| "Data Abstraction and Hierarchy" | Barbara Liskov | 1987 | LSP origin (OOPSLA '87 keynote) |
| "A Behavioral Notion of Subtyping" | Barbara Liskov, Jeannette Wing | 1994 | Formal LSP definition (ACM TOPLAS) |
| "The Liskov Substitution Principle" | Robert C. Martin | 1996 | Square/Rectangle problem (C++ Report) |
| "The Interface Segregation Principle" | Robert C. Martin | 1996 | ISP definition and Xerox case (C++ Report) |
| "The Dependency Inversion Principle" | Robert C. Martin | 1996 | DIP definition (C++ Report) |

**PDF Archives:**

| Paper | URL |
|-------|-----|
| Martin C++ Report articles | [UT Austin CS](https://www.cs.utexas.edu/~downing/papers/) |
| Liskov-Wing 1994 | [CMU Wing Publications](https://www.cs.cmu.edu/~wing/publications/LiskovWing94.pdf) |
| Liskov 1987 | [Tufts CS Archive](https://www.cs.tufts.edu/~nr/cs257/archive/barbara-liskov/data-abstraction-and-hierarchy.pdf) |

**Research Studies:**

**"Applying the Single Responsibility Principle in Industry"**
Proceedings of the 23rd International Conference on Evaluation and Assessment in Software Engineering (EASE 2019)
Industrial case study on two large-scale software systems (1,500+ classes) examining SRP violations.
ACM Digital Library: [doi.org/10.1145/3319008.3320125](https://dl.acm.org/doi/10.1145/3319008.3320125)

**Microsoft Learn, "Dangers of Violating SOLID Principles in C#"** (MSDN Magazine, May 2014)
Documents how SOLID violations lead to code complexity, testing difficulty, merge conflicts, and coupling.
Source: [Microsoft Learn Archive](https://learn.microsoft.com/en-us/archive/msdn-magazine/2014/may/csharp-best-practices-dangers-of-violating-solid-principles-in-csharp)

---

## Thought Leaders

### Donald Knuth

**Agent**: `knuth` (algorithmic complexity)

### Primary Source

Knuth, Donald E. "Structured Programming with go to Statements." *ACM Computing Surveys* 6, no. 4 (December 1974): 261-301.

- **DOI**: [10.1145/356635.356640](https://doi.org/10.1145/356635.356640)
- **Context**: Written in response to Dijkstra's "Go To Statement Considered Harmful" (1968), this paper argues for careful, measured use of goto statements in performance-critical code.

### The Quote

> "There is no doubt that the grail of efficiency leads to abuse. Programmers waste enormous amounts of time thinking about, or worrying about, the speed of noncritical parts of their programs, and these attempts at efficiency actually have a strong negative impact when debugging and maintenance are considered. We should forget about small efficiencies, say about 97% of the time: **premature optimization is the root of all evil**."

The quote continues:

> "Yet we should not pass up our opportunities in that critical 3%."

### Attribution Note

Knuth himself referred to this as "Hoare's Dictum" in "The Errors of TeX" (*Software--Practice & Experience* 19:7, July 1989, pp. 607-685). However, when asked, Tony Hoare suggested Dijkstra might deserve credit. The earliest traceable source remains this 1974 Knuth paper.

### Application to Architecture

The Guild's `knuth` agent invokes this principle inversely: **architectural** complexity decisions are not premature optimization. The quote warns against micro-optimization of non-critical paths, not against understanding algorithmic complexity early. O(n) vs O(n^2) matters at design time. Loop unrolling can wait.

---

## Edsger W. Dijkstra

**Agent**: `dijkstra` (formal correctness)

### Primary Sources

**The Humble Programmer** (1972)

Dijkstra, Edsger W. "The Humble Programmer." *Communications of the ACM* 15, no. 10 (October 1972): 859-866.

- **DOI**: [10.1145/355604.361591](https://doi.org/10.1145/355604.361591)
- **EWD Archive**: [EWD340](https://www.cs.utexas.edu/~EWD/transcriptions/EWD03xx/EWD340.html)
- **Context**: ACM Turing Award lecture, delivered August 14, 1972, Boston.

**How Do We Tell Truths That Might Hurt?** (1975)

Dijkstra, Edsger W. "How do we tell truths that might hurt?" EWD498, June 18, 1975.

- **EWD Archive**: [EWD498](https://www.cs.utexas.edu/~EWD/transcriptions/EWD04xx/EWD498.html)
- **Also in**: *Selected Writings on Computing: A Personal Perspective* (Springer, 1982).

### The Quotes

**On Abstraction** (used by `dijkstra` agent):

> "The purpose of abstraction is not to be vague, but to create a new semantic level in which one can be absolutely precise."

*Note*: Sometimes rendered as "The purpose of abstracting..." The source is from Dijkstra's collection of aphorisms.

**On Simplicity**:

> "Simplicity is prerequisite for reliability."

**On the Programmer's Task** (from "The Humble Programmer"):

> "The competent programmer is fully aware of the strictly limited size of his own skull; he therefore approaches the programming task in full humility, and among other things he avoids clever tricks like the plague."

**On Tools** (from EWD498):

> "The tools we use have a profound (and devious!) influence on our thinking habits, and, therefore, on our thinking abilities."

### Application to Architecture

The Guild's `dijkstra` agent embodies his approach to correctness: preconditions, postconditions, invariants, and proof sketches. His emphasis on humility informs the agent's focus on formal verification rather than intuition. "It seems to work" is never sufficient.

---

## Leslie Lamport

**Agent**: `lamport` (distributed systems)

### Primary Sources

**Time, Clocks, and the Ordering of Events in a Distributed System** (1978)

Lamport, Leslie. "Time, Clocks, and the Ordering of Events in a Distributed System." *Communications of the ACM* 21, no. 7 (July 1978): 558-565.

- **DOI**: [10.1145/359545.359563](https://doi.org/10.1145/359545.359563)
- **Awards**: PODC Influential Paper Award (2000), ACM SIGOPS Hall of Fame Award (2007)
- **Context**: One of the most cited papers in Computer Science. Introduced Lamport timestamps and the "happened-before" relation.

**The Part-Time Parliament** (1998)

Lamport, Leslie. "The Part-Time Parliament." *ACM Transactions on Computer Systems* 16, no. 2 (May 1998): 133-169.

- **DOI**: [10.1145/279227.279229](https://doi.org/10.1145/279227.279229)
- **PDF**: [lamport-paxos.pdf](https://lamport.azurewebsites.net/pubs/lamport-paxos.pdf)
- **Context**: First submitted in 1990. Describes the Paxos consensus algorithm through the allegory of a Greek parliament.

**Paxos Made Simple** (2001)

Lamport, Leslie. "Paxos Made Simple." *ACM SIGACT News* 32, no. 4 (December 2001): 18-25.

- **PDF**: [paxos-simple.pdf](https://lamport.azurewebsites.net/pubs/paxos-simple.pdf)
- **Context**: Plain-English explanation after the original paper's allegory proved difficult for readers.

### Key Insight

From "Time, Clocks":

> "The concept of one event happening before another in a distributed system is examined, and is shown to define a partial ordering of the events."

This partial ordering -- not total ordering -- is the fundamental insight. Distributed systems cannot have a global clock.

### Application to Architecture

The Guild's `lamport` agent asks: "What happens when the network lies? When clocks disagree?" His work proves that local assumptions in distributed systems are mathematically invalid. The catchphrase "Time is an illusion. Latency is real." captures Lamport's core insight: you cannot reason about distributed systems as if they were local.

---

## G.K. Chesterton

**Agent**: `chesterton` (historical context)

### Primary Source

Chesterton, Gilbert Keith. *The Thing: Why I Am a Catholic*. London: Sheed & Ward, 1929.

- **Chapter**: "The Drift from Domesticity"
- **Full text**: [Gutenberg](https://www.gutenberg.org/ebooks/author/80) (public domain)

### The Quote

> "In the matter of reforming things, as distinct from deforming them, there is one plain and simple principle; a principle which will probably be called a paradox. There exists in such a case a certain institution or law; let us say, for the sake of simplicity, a fence or gate erected across a road. The more modern type of reformer goes gaily up to it and says, 'I don't see the use of this; let us clear it away.' To which the more intelligent type of reformer will do well to answer: 'If you don't see the use of it, I certainly won't let you clear it away. Go away and think. Then, when you can come back and tell me that you do see the use of it, I may allow you to destroy it.'"

### Common Paraphrase

> "Don't ever take a fence down until you know the reason it was put up."

This paraphrase was a favorite of John F. Kennedy (noted in *Bartlett's Familiar Quotations*).

### Application to Architecture

The Guild's `chesterton` agent is the voice of historical context. Before removing "dead" code, understand why it exists. That mysterious `sleep(100)` might be a race condition fix. That "unused" module might be a production hotfix from 2019. The agent's process: `git blame`, commit messages, issue search, documentation -- understand the fence before removing it.

---

## Nassim Nicholas Taleb

**Agent**: `taleb` (resilience and antifragility)

### Primary Source

Taleb, Nassim Nicholas. *Antifragile: Things That Gain from Disorder*. New York: Random House, 2012.

- **ISBN**: 978-0-8129-7968-8 (paperback)
- **Series**: Part of the *Incerto* series (includes *Fooled by Randomness*, *The Black Swan*, *Skin in the Game*)

### Key Concepts

**Antifragility**:

> "Some things benefit from shocks; they thrive and grow when exposed to volatility, randomness, disorder, and stressors and love adventure, risk, and uncertainty."

The book distinguishes three categories:

| Category | Response to Stress |
|----------|-------------------|
| Fragile | Harmed by disorder |
| Robust | Unaffected by disorder |
| Antifragile | Gains from disorder |

**Black Swan** (from *The Black Swan*, 2007):

A high-impact, hard-to-predict event that is rationalized in hindsight. Software examples: cascade failures, security breaches, market crashes.

### Application to Architecture

The Guild's `taleb` agent asks: "What's the Black Swan? If AWS us-east-1 vanishes, does this degrade gracefully or explode?" His framework shifts thinking from "prevent all failures" to "benefit from stress." Systems should be antifragile where possible: circuit breakers that trip early, chaos engineering that strengthens, redundancy that exercises itself.

---

## Lotfi A. Zadeh

**Agent**: `lotfi` (fuzzy scoring and trade-offs)

### Primary Source

Zadeh, Lotfi A. "Fuzzy Sets." *Information and Control* 8, no. 3 (June 1965): 338-353.

- **DOI**: [10.1016/S0019-9958(65)90241-X](https://doi.org/10.1016/S0019-9958(65)90241-X)
- **Publisher**: Academic Press

### Key Concept

> "A fuzzy set is a class of objects with a continuum of grades of membership. Such a set is characterized by a membership (characteristic) function which assigns to each object a grade of membership ranging between zero and one."

Classical set theory: an element is either in a set or not (binary). Fuzzy set theory: an element has a *degree* of membership (gradient).

### Application to Architecture

The Guild's `lotfi` agent handles deadlocks between competing concerns. When `dijkstra` says BLOCK and `k` says APPROVE, binary verdicts fail. Fuzzy scoring enables nuanced trade-off analysis:

- Consistency: 0.8
- Availability: 0.3
- Complexity: 0.6

This allows verdicts like "acceptable for internal tools, not for payment processing" -- degrees of truth, not binary choices.

---

## Foundational Software Engineering

### David Parnas

**Core Contribution**: Information hiding and module decomposition

### Primary Source

Parnas, David L. "On the Criteria To Be Used in Decomposing Systems into Modules." *Communications of the ACM* 15, no. 12 (December 1972): 1053-1058.

- **DOI**: [10.1145/361598.361623](https://doi.org/10.1145/361598.361623)
- **Affiliation**: Department of Computer Science, Carnegie-Mellon University
- **Original Memo**: Written 1971 as Carnegie Mellon memo
- **ACM Digital Library**: https://dl.acm.org/doi/10.1145/361598.361623

### Key Quotes

**On Module Decomposition**:

> "We have tried to demonstrate by these examples that it is almost always incorrect to begin the decomposition of a system into modules on the basis of a flowchart. We propose instead that one begins with a list of difficult design decisions or design decisions which are likely to change. Each module is then designed to hide such a decision from the others."

**On Information Hiding**:

> "Every module in the second decomposition is characterized by its knowledge of a design decision which it hides from all others. Its interface or definition was chosen to reveal as little as possible about its inner workings."

### Impact

Three decades after Parnas first articulated information hiding, he argued it remains "the most important and basic software design principle." In the 20th Anniversary edition of *The Mythical Man-Month*, Fred Brooks concludes: "Parnas was right, and I was wrong about information hiding."

### Application to Architecture

Module boundaries should be drawn around design decisions likely to change, not around processing steps. This principle underpins interface design, encapsulation, and the separation of concerns that forms the foundation of modern software architecture.

---

### Alan Kay

**Core Contribution**: Object-oriented programming, Smalltalk, personal computing

### Recognition

Kay, Alan C. ACM A.M. Turing Award, 2003.

- **Citation**: "For pioneering many of the ideas at the root of contemporary object-oriented programming languages, leading the team that developed Smalltalk, and for fundamental contributions to personal computing."
- **ACM Profile**: https://amturing.acm.org/award_winners/kay_3972189.cfm

### Key Quotes

**On Design Simplicity**:

> "Simple things should be simple, complex things should be possible."

- **Origin**: Coined at Xerox PARC circa 1971 during discussions about children, end-users, user interfaces, and programming languages. Kay confirmed the origin in a September 17, 1998 email to Peter W. Lount.
- **Context**: Emerged from Smalltalk design philosophy -- the language needed to work intuitively for children and end-users while remaining powerful enough that the entire system could be written in itself.

**On Inventing the Future**:

> "The best way to predict the future is to invent it."

- **Origin**: Spoken at Xerox PARC in 1971 during a meeting with Xerox executives. Kay stated: "In a fit of passion I uttered the quote!"
- **Note**: Similar sentiments appear in Dennis Gabor's *Inventing the Future* (1963): "The future cannot be predicted, but futures can be invented."

### Smalltalk Contributions

Smalltalk was the first complete dynamic object-oriented programming language and development environment. At Xerox PARC, Kay led development and coined the term "object-oriented." The visual programming environment, revolutionary at the time, is now conventional. Overlapping screen windows, a component of the graphical user interface, emerged from Kay's "user-centered" approach to computing.

### Application to Architecture

Kay's design philosophy -- simplicity for the common case, power for the edge case -- informs API design and system interfaces. The layered disclosure model (simple surface, complex depths) appears throughout well-designed systems.

---

### Andrew Hunt & David Thomas

**Core Contribution**: Pragmatic software development principles, DRY, orthogonality

### Primary Sources

**First Edition** (1999):

Hunt, Andrew, and David Thomas. *The Pragmatic Programmer: From Journeyman to Master*. Reading, MA: Addison-Wesley, 1999.

- **ISBN-10**: 020161622X
- **ISBN-13**: 978-0201616224
- **Publisher**: Addison-Wesley Professional

**Second Edition** (2019):

Thomas, David, and Andrew Hunt. *The Pragmatic Programmer: Your Journey to Mastery* (20th Anniversary Edition). Boston: Addison-Wesley, 2019.

- **ISBN-10**: 0135957052
- **ISBN-13**: 978-0135957059
- **Pages**: 352
- **Publisher**: Addison-Wesley Professional (by arrangement with The Pragmatic Bookshelf)

### Key Concepts

**DRY (Don't Repeat Yourself)**:

> "Every piece of knowledge must have a single, unambiguous, authoritative representation within a system."

- **Location**: Chapter 2, "A Pragmatic Approach," Topic 9: "DRY: The Evils of Duplication"
- **Scope**: Applies broadly to database schemas, test plans, build systems, and documentation -- not just code.

**Orthogonality**:

> "Eliminate Effects Between Unrelated Things" (Tip 13)

Two or more things are orthogonal if changes in one do not affect any of the others. Components should be self-contained, independent, and have a single, well-defined purpose. Combined with DRY, orthogonality produces systems that are more flexible, understandable, and easier to debug, test, and maintain.

### Other Named Concepts

The book named or popularized several practices including rubber duck debugging and the broken windows theory applied to software.

### Application to Architecture

DRY and orthogonality are foundational architectural principles. DRY prevents knowledge fragmentation and inconsistency. Orthogonality ensures that changes remain localized, reducing blast radius and cognitive load. Together they form the basis for maintainable system design.

---

### Frederick P. Brooks Jr.

**Core Contribution**: Software project management, Brooks' Law, essential vs. accidental complexity

### Primary Sources

**The Book**:

Brooks, Frederick P., Jr. *The Mythical Man-Month: Essays on Software Engineering*. Reading, MA: Addison-Wesley, 1975.

- **Anniversary Edition** (1995): Addison-Wesley, ISBN 0-201-83595-9
- **ACM Reference**: https://dl.acm.org/doi/10.5555/207583

**The Essay**:

Brooks, Frederick P., Jr. "No Silver Bullet -- Essence and Accident in Software Engineering." *Computer* 20, no. 4 (April 1987): 10-19.

- **Original Presentation**: IFIP Congress, 1986
- **Reprinted in**: Anniversary Edition of *The Mythical Man-Month* (1995)
- **PDF**: https://worrydream.com/refs/Brooks_1986_-_No_Silver_Bullet.pdf

### Brooks' Law

> "Adding manpower to a late software project makes it later."

Brooks developed this observation from his experience managing IBM's OS/360 development. When the project fell behind, he added more programmers -- a decision he later concluded had delayed the project further.

**Contributing factors**:
1. **Ramp-up time**: New people must be educated about existing work, diverting resources from production
2. **Communication overhead**: Channels increase with the square of people; doubling the team quadruples coordination complexity
3. **Limited divisibility**: "While it takes one woman nine months to make one baby, nine women can't make a baby in one month"

Brooks called this an "outrageous oversimplification" but one that captures the general rule.

### Essential vs. Accidental Complexity

From "No Silver Bullet," following Aristotle:

- **Essential complexity**: Inherent in the nature of the problem. If users want 30 features, those 30 features are essential. Nothing can remove it.
- **Accidental complexity**: Self-inflicted difficulties that are not inherent to the problem. Engineers create it; engineers can fix it.

> "The complexity of software is an essential property, not an accidental one. Hence descriptions of a software entity that abstract away its complexity often abstract away its essence."

**The thesis**: High-level languages reduced accidental complexity substantially. Today's programmers spend most of their time on essential complexity. Therefore, eliminating remaining accidental complexity cannot yield order-of-magnitude improvements.

> "But, as we look to the horizon of a decade hence, we see no silver bullet. There is no single development, in either technology or management technique, which by itself promises even one order of magnitude improvement in productivity, in reliability, in simplicity."

### Later Reflection

In "'No Silver Bullet' Refired" (1995): "It is my opinion, and that is all, that the accidental or representational part of the work is now down to about half or less of the total."

### Application to Architecture

Brooks' framework distinguishes problems worth solving (accidental complexity) from problems that must be managed (essential complexity). Architectural decisions should target accidental complexity -- unnecessary coupling, poor abstractions, technology mismatches -- while accepting that essential complexity cannot be designed away, only organized well.

---

# Event-Driven Architecture Patterns

Authoritative references for event-driven patterns documented in `skills/architecture/references/event-driven.md`.

---

## Command Query Separation (CQS)

### Original Source

Meyer, Bertrand. *Object-Oriented Software Construction*. Prentice Hall, 1988. Second edition, 1997.

- **ISBN**: 978-0-13-629155-8 (2nd ed.)
- **Publisher**: Prentice Hall PTR
- **Context**: Bertrand Meyer developed CQS as part of his work on the Eiffel programming language. The book is one of the most influential OO books of the early OO era.

### The Principle

Every method should either be a **command** that performs an action, or a **query** that returns data to the caller, but not both.

> "Asking a question should not change the answer."

- **Queries**: Return a result and do not change the observable state of the system (free of side effects)
- **Commands**: Change the state of a system but do not return a value

### Acknowledged Exception

Meyer himself noted that `pop()` on a stack is a useful idiom that violates CQS -- a query that modifies state. Practical pragmatism over dogmatic purity.

### Why This Matters

CQS is the intellectual foundation for CQRS. Understanding Meyer's original principle clarifies what Greg Young generalized to the architectural level.

---

## CQRS (Command Query Responsibility Segregation)

### Original Source

Young, Greg. "CQRS Documents." November 2010.

- **Primary PDF**: [cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf](https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf)
- **Alternative**: [cqrs.wordpress.com/wp-content/uploads/2010/11/cqrs_documents.pdf](https://cqrs.wordpress.com/wp-content/uploads/2010/11/cqrs_documents.pdf)
- **E-book version**: [github.com/keyvanakbary/cqrs-documents](https://github.com/keyvanakbary/cqrs-documents)
- **Context**: Originally a class manual, this document comprehensively covers CQRS, Event Sourcing, and related patterns.

### The Definition

> "CQRS is simply the creation of two objects where there was previously only one."

From a 2010 post titled "CQRS, Task Based UIs, Event Sourcing agh!"

### Historical Context

CQRS was originally considered just an extension of Meyer's CQS. For a long time it was discussed as "CQS at a higher level." Eventually, after much confusion between the two concepts, it was correctly deemed to be a different pattern.

### Secondary Source

Fowler, Martin. "CQRS." *martinfowler.com*, July 14, 2011.

- **URL**: [martinfowler.com/bliki/CQRS.html](https://martinfowler.com/bliki/CQRS.html)
- **Quote**: "Greg Young was the first person I heard talking about this approach."
- **Note**: Fowler also credits Udi Dahan as another advocate with detailed descriptions.

### Greg Young on CQRS vs Event Sourcing (2016)

From "A Decade of DDD, CQRS, Event Sourcing" talk:

> "You need to look at CQRS not as being the main thing. CQRS was a product of its time and meant to be a stepping stone towards the ideas of Event Sourcing."

---

## Event Sourcing

### Original Naming

Fowler, Martin. "Event Sourcing." *martinfowler.com*, December 12, 2005.

- **URL**: [martinfowler.com/eaaDev/EventSourcing.html](https://martinfowler.com/eaaDev/EventSourcing.html)
- **Context**: Part of the "Further Enterprise Application Architecture" development writing. Remains in draft form but introduced the term and concept to wide audience.

### The Definition

> "The fundamental idea of Event Sourcing is ensuring every change to the state of an application is captured in an event object, and that these event objects are themselves stored in the sequence they were applied for the same lifetime as the application state itself."

### Greg Young's Elaboration

Greg Young introduced Event Sourcing to the public around the same time as CQRS (2010). He uses the term Event Sourcing to mean "the rebuilding of objects based on events."

- **Source**: CQRS Documents (2010)
- **EventStore**: Greg Young is the lead architect of Event Store, the purpose-built event sourcing database.

### Key Distinction

> "CQRS is about isolating reads from writes into different code paths. Event Sourcing is about using events to record state."

State transitions are modelled within the domain using events. Events are facts about what happened -- they are never updated or deleted, they are immutable.

---

## Saga Pattern

### Original Source

Garcia-Molina, Hector, and Kenneth Salem. "Sagas." *Proceedings of the 1987 ACM SIGMOD International Conference on Management of Data* (SIGMOD '87). San Francisco, CA, May 27-29, 1987, pp. 249-259.

- **DOI**: [10.1145/38713.38742](https://doi.org/10.1145/38713.38742)
- **ACM DL**: [dl.acm.org/doi/10.1145/38713.38742](https://dl.acm.org/doi/10.1145/38713.38742)
- **Full PDF**: [cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf](https://www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf)
- **Also in**: *ACM SIGMOD Record* 16, no. 3 (December 1987): 249-259.

### The Problem

> "Long lived transactions (LLTs) hold on to database resources for relatively long periods of time, significantly delaying the termination of shorter and more common transactions."

### The Solution

> "A LLT is a saga if it can be written as a sequence of transactions that can be interleaved with other transactions. The database management system guarantees that either all the transactions in a saga are successfully completed or compensating transactions are run to amend a partial execution."

### Historical Note

The original paper was written for a **single relational database**, defining a way to handle system failures for long-running transactions. The microservices community adopted the same mechanism for distributed transactions, hence "distributed sagas."

### Key Insight

Sagas trade atomicity for progress. Instead of blocking other transactions while a long-lived transaction completes, sagas allow interleaving with compensating transactions to handle failures.

---

## Transactional Outbox Pattern

### Primary Source

Richardson, Chris. "Pattern: Transactional Outbox." *microservices.io*.

- **URL**: [microservices.io/patterns/data/transactional-outbox.html](https://microservices.io/patterns/data/transactional-outbox.html)
- **Book**: Richardson, Chris. *Microservices Patterns: With Examples in Java*. Manning Publications, 2018. ISBN: 978-1-61729-454-9.
- **Context**: Chris Richardson is the creator of the original CloudFoundry.com and author of *POJOs in Action*. He is the publisher of microservices.io.

### The Problem

> "Without using 2PC, sending a message in the middle of a transaction is not reliable. There's no guarantee that the transaction will commit. Similarly, if a service sends a message after committing the transaction there's no guarantee that it won't crash before sending the message."

### The Solution

> "A service command typically needs to create/update/delete aggregates in the database and send messages/events to a message broker... The command must atomically update the database and send messages in order to avoid data inconsistencies and bugs."

The pattern: Write the message to an OUTBOX table as part of the same database transaction. A separate message relay process publishes events from the outbox to the message broker.

### Related Patterns

- **Polling Publisher**: Poll the outbox table for unpublished messages
- **Transaction Log Tailing**: Use CDC (Change Data Capture) to read from the transaction log

### Udi Dahan's Contribution

Dahan, Udi. "Reliable Messaging Without Distributed Transactions." Particular Software.

- **Video**: [particular.net/videos/messaging-without-dtc](https://particular.net/videos/messaging-without-dtc)
- **Context**: Explains the outbox pattern in depth, including implementation in NServiceBus.

Key insight from Dahan: Use a table of message IDs for duplicate detection, and a table of outgoing messages for replay. If a message is a duplicate, replay the sending of all outgoing messages with the same message IDs so downstream subscribers' deduplication logic works correctly.

---

## Idempotency in Distributed Systems

### Academic Foundation

Ramalingam, G., and Kapil Vaswani. "Fault Tolerance via Idempotence." *Proceedings of the 40th Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages* (POPL '13). Rome, Italy, January 2013.

- **DOI**: [10.1145/2429069.2429100](https://doi.org/10.1145/2429069.2429100)
- **PDF**: [microsoft.com/en-us/research/wp-content/uploads/2016/02/popl38-ramalingam.pdf](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/popl38-ramalingam.pdf)
- **Affiliation**: Microsoft Research

### The Challenge

> "Writing applications for distributed systems is challenging because of the pitfalls of distribution such as process failures, communication failures, asynchrony and concurrency... One common requirement and challenge is the need for distributed applications that are idempotent."

### The Definition

> "Idempotence ensures that the application functions correctly even when clients send duplicate requests, perhaps because the application failed to generate a response due to process failures, or because the response was generated but lost."

### Practical Implementation

Helland, Pat. "Life beyond Distributed Transactions: an Apostate's Opinion." *CIDR 2007*, pp. 132-141.

- **PDF**: [ics.uci.edu/~cs223/papers/cidr07p15.pdf](https://ics.uci.edu/~cs223/papers/cidr07p15.pdf)
- **Republished**: *ACM Queue*, 2016. [queue.acm.org/detail.cfm?id=3025012](https://queue.acm.org/detail.cfm?id=3025012)
- **About the Author**: Pat Helland has been implementing transaction systems, databases, distributed systems, and messaging systems since 1978. Currently at Salesforce.

### Key Quote on Idempotency

> "Processing messages that are not naturally idempotent requires ensuring that each message is processed at most once (i.e., the substantive impact of the message must happen at most once)."

Messages that cause substantive changes are not naturally idempotent. The application must include mechanisms to ensure idempotence -- typically by remembering that the message has been processed.

### The Activity Pattern

Helland introduces "Activity" -- responsible for remembering the history of interactions. This history needs to answer: "Did I process that message already?"

---

## Message Delivery Semantics

### The Three Guarantees

| Guarantee | Definition | Trade-off |
|-----------|------------|-----------|
| **At Most Once** | Messages delivered 0 or 1 times | Lowest latency, risk of data loss |
| **At Least Once** | Messages delivered 1 or more times | Guaranteed delivery, requires idempotent consumers |
| **Exactly Once** | Messages delivered exactly 1 time | Requires idempotency + deduplication (effectively "exactly once effect") |

### The Fundamental Problem

True "exactly once" delivery is impossible in distributed systems due to the Two Generals Problem.

### Original Paper on Two Generals

Akkoyunlu, E.A., K. Ekanadham, and R.V. Huber. "Some Constraints and Trade-offs in the Design of Network Communications." *Proceedings of the Fifth ACM Symposium on Operating Systems Principles* (SOSP '75). Austin, Texas, November 1975, pp. 67-74.

- **DOI**: [10.1145/800213.806523](https://doi.org/10.1145/800213.806523)
- **Context**: The problem was originally described using gangsters, not generals.

### The Name

Gray, Jim. "Notes on Data Base Operating Systems." In *Operating Systems: An Advanced Course*, Lecture Notes in Computer Science, vol 60. Springer, 1978, pp. 393-481.

- **DOI**: [10.1007/3-540-08755-9_9](https://doi.org/10.1007/3-540-08755-9_9)
- **Context**: Jim Gray named it the "Two Generals Paradox" in this 1978 paper.

### Significance

> "The Two Generals' Problem was the first computer communication problem to be proven to be unsolvable."

Systems achieve "exactly once effect" through at-least-once delivery combined with idempotent processing.

---

# Chaos Engineering

**Related**: `plugins/arch-guild/skills/operations/references/chaos-patterns.md`

Chaos Engineering is the discipline of experimenting on a system in order to build confidence in the system's capability to withstand turbulent conditions in production. This bibliography traces its evolution from early fault injection research through Netflix's formalization to modern practice.

---

## Timeline of Chaos Engineering Evolution

| Year | Event | Significance |
|------|-------|--------------|
| 1972 | Harlan Mills (IBM) proposes fault seeding | Earliest ancestor of software fault injection |
| 1970s | Hardware fault injection emerges | HWIFI techniques for reliability testing |
| 1990 | FIAT tool at Carnegie Mellon | Academic formalization of fault injection |
| 1992 | FERRARI tool published | Software-based fault injection framework |
| 1994 | FTAPE tool published | Fault tolerance measurement methodology |
| 2006 | Google DiRT program founded | Disaster Recovery Testing at Google scale |
| Early 2000s | Jesse Robbins creates GameDay at Amazon | First structured failure injection program |
| 2008 | Netflix migrates to AWS | Database corruption triggers cloud move |
| 2010 | Chaos Monkey created at Netflix | Greg Orzell and team build random termination tool |
| July 2011 | Netflix Simian Army announced | Public debut of chaos engineering tools |
| July 2012 | Chaos Monkey open-sourced | Apache 2.0 license on GitHub |
| September 2012 | "Resilience Engineering" roundtable | ACM Queue article defining the practice |
| February 2017 | Chaos Engineering arXiv paper | IEEE Software publication formalizes discipline |
| 2017 | principlesofchaos.org launched | Canonical definition of principles |
| 2020 | "Chaos Engineering" book (O'Reilly) | Comprehensive practitioner guide |

---

## Foundational Documents

### The Principles of Chaos Engineering

**Source**: principlesofchaos.org (Last updated: December 2017)

**Authors**: Ali Basiri, Niosha Behnam, Ruud de Rooij, Lorin Hochstein, Luke Kosewski, Justin Reynolds, Casey Rosenthal

**Key Definition**:

> "Chaos Engineering is the discipline of experimenting on a system in order to build confidence in the system's capability to withstand turbulent conditions in production."

**The Four Steps**:

1. Start by defining "steady state" as some measurable output of a system that indicates normal behavior
2. Hypothesize that this steady state will continue in both the control group and the experimental group
3. Introduce variables that reflect real-world events (servers crash, hard drives malfunction, network connections severed)
4. Try to disprove the hypothesis by looking for a difference in steady state between control and experimental groups

**Advanced Principles**:

- Build a hypothesis around steady state behavior
- Vary real-world events
- Run experiments in production
- Automate experiments to run continuously
- Minimize blast radius

**URL**: https://principlesofchaos.org/

---

### Chaos Engineering (arXiv)

Basiri, Ali, Niosha Behnam, Ruud de Rooij, Lorin Hochstein, Luke Kosewski, Justin Reynolds, and Casey Rosenthal. "Chaos Engineering." *IEEE Software* 34, no. 3 (May-June 2017): 35-41.

- **arXiv**: [1702.05843](https://arxiv.org/abs/1702.05843) (submitted February 20, 2017)
- **DOI**: 10.1109/MS.2017.55
- **Citations**: 218+ (Semantic Scholar)

**Abstract**:

> "Modern software-based services are implemented as distributed systems with complex behavior and failure modes. Many large tech organizations are using experimentation to verify the reliability of such systems. We use the term 'Chaos Engineering' to refer to this approach."

**Context**: This paper formalized the discipline that Netflix engineers had been practicing since 2010, providing the academic foundation for chaos engineering as a field.

---

## Netflix Origins

### The Netflix Simian Army (2011)

Izrailevsky, Yury, and Ariel Tseitlin. "The Netflix Simian Army." *Netflix Tech Blog*, July 19, 2011.

- **Original URL**: http://techblog.netflix.com/2011/07/netflix-simian-army.html
- **Medium Archive**: https://netflixtechblog.com/the-netflix-simian-army-16e57fbab116

**Key Quote**:

> "We have found that the best defense against major unexpected failures is to fail often. By frequently causing failures, we force our services to be built in a way that is more resilient."

**The Flat Tire Analogy**:

> "Imagine getting a flat tire. Even if you have a spare tire in your trunk, do you know if it is inflated? Do you have the tools to change it? [...] Chaos Monkey is a tool that randomly disables our production instances to make sure we can survive this common type of failure without any customer impact."

**The Name**:

> "The name comes from the idea of unleashing a wild monkey with a weapon in your data center (or cloud region) to randomly shoot down instances and chew through cables."

---

### Chaos Monkey Open Source Release (2012)

Bennett, Cory, and Ariel Tseitlin. "Netflix Chaos Monkey Released into the Wild." *Netflix Tech Blog*, July 30, 2012.

- **GitHub**: https://github.com/Netflix/chaosmonkey
- **License**: Apache 2.0
- **Original Repository**: https://github.com/Netflix/SimianArmy (archived)

**Key Quote**:

> "We have found that the best defense against major unexpected failures is to fail often. By frequently causing failures, we force our services to be built in a way that is more resilient."

---

### The Simian Army Members

| Tool | Purpose | First Announced |
|------|---------|-----------------|
| **Chaos Monkey** | Random instance termination | 2010 (internal), 2011 (public) |
| **Latency Monkey** | Artificial delays in RESTful calls | 2011 |
| **Conformity Monkey** | Find non-compliant instances | 2011 |
| **Doctor Monkey** | Health checks, unhealthy instance removal | 2011 |
| **Janitor Monkey** | Cleanup unused resources | 2011 |
| **Security Monkey** | Find security violations | 2011 |
| **Chaos Gorilla** | Kill entire availability zone | 2011 |
| **Chaos Kong** | Kill entire region | Later addition |

---

## GameDay Origins

### Jesse Robbins at Amazon

**Creator**: Jesse Robbins ("Master of Disaster")

**Context**: Robbins created GameDay at Amazon in the early 2000s while responsible for website availability for every Amazon-branded property.

**Background**: Robbins trained as a firefighter and EMT, serving as a volunteer and Emergency Manager including deployment during Hurricane Katrina. He adapted emergency response principles to software systems.

**Key Quote**:

> "The key to building resilient systems is accepting that failure happens. There's just no getting around it. That applies to the software discipline, as well as to the systems management and architectural disciplines. It also applies to managing people. It's only after you've accepted the reality that failure is inevitable that you can begin the journey toward a truly resilient system."

**Recognition**: MIT Technology Review TR35 Award (2011) for "transforming the way Web companies design and manage complex networks of servers and software."

**Wikipedia**: https://en.wikipedia.org/wiki/Jesse_Robbins

---

### Resilience Engineering: Learning to Embrace Failure (2012)

Robbins, Jesse, Kripa Krishnan, John Allspaw, and Thomas A. Limoncelli. "Resilience Engineering: Learning to Embrace Failure." *ACM Queue* 10, no. 9 (September 2012): 20-28.

- **URL**: https://queue.acm.org/detail.cfm?id=2371297
- **Also in**: *Communications of the ACM* 55, no. 11 (November 2012): 40-47

**Key Quote**:

> "At the core of every resilience program at companies like Google, Facebook, Etsy, Flickr, Yahoo, or Amazon is the understanding that when engineering systems at Internet scale, the best you can hope for is to build a reliable software platform on top of components that are completely unreliable, putting you in an environment where complex failures are both inevitable and unpredictable."

**Participants**:
- **Jesse Robbins**: Architect of GameDay at Amazon, "Master of Disaster"
- **Kripa Krishnan**: Technical Program Manager, Google DiRT program
- **John Allspaw**: VP Engineering at Etsy, co-author "Web Operations"
- **Thomas A. Limoncelli**: Site Reliability Engineer at Google, moderator

---

## Google DiRT Program

### Weathering the Unexpected (2012)

Krishnan, Kripa. "Weathering the Unexpected." *Communications of the ACM* 55, no. 11 (November 2012): 48-52.

- **URL**: https://cacm.acm.org/magazines/2012/11/156583-weathering-the-unexpected/fulltext
- **DOI**: 10.1145/2366316.2366332

**Key Quote**:

> "The most important of those lessons is that an untested disaster recovery plan isn't really a plan at all."

**About DiRT**:

Google's DiRT (Disaster Recovery Testing) program was founded by site reliability engineers in 2006. DiRT intentionally instigates failures in critical technology systems and business processes to expose unaccounted-for risks.

**Methodology**:

> "DiRT tests both Google's technical robustness, by breaking live systems, and our operational resilience by explicitly preventing critical personnel, area experts, and leaders from participating."

**Evolution**:

- Started with individual groups testing failure scenarios specific to their service
- Progressed to simulating major outages (primary source-control management servers)
- Eventually simulated major disasters (Bay Area "earthquake" taking down a data center)

---

### 10 Years of Crashing Google (2015)

Krishnan, Kripa. "10 Years of Crashing Google." USENIX LISA Conference, 2015.

- **URL**: https://www.usenix.org/conference/lisa15/conference-program/presentation/krishnan

**Context**: Retrospective on DiRT program evolution from 2006-2015.

---

## Books

### Chaos Engineering: System Resiliency in Practice (2020)

Rosenthal, Casey, and Nora Jones, eds. *Chaos Engineering: System Resiliency in Practice*. Sebastopol, CA: O'Reilly Media, 2020.

- **ISBN**: 978-1-4920-4386-7 (paperback)
- **ISBN**: 978-1-4920-4385-0 (ebook)
- **O'Reilly**: https://www.oreilly.com/library/view/chaos-engineering/9781492043850/

**From the Introduction**:

> "The story begins at Netflix in 2008, when they made a public move from the datacenter to the cloud following a major database corruption event that left Netflix unable to ship DVDs for three days. The thinking at the time was that the datacenter locked them into an architecture of single points of failure, and moving to the cloud would necessitate horizontally scaled components to decrease these single points of failure."

**About the Editors**:
- **Casey Rosenthal**: CEO and cofounder of Verica; formerly engineering manager of Chaos Engineering Team at Netflix
- **Nora Jones**: Cofounder and CEO of Jeli (acquired by PagerDuty 2023); formerly chaos engineer at Netflix and Slack

**Chapter 5** covers Google DiRT in detail.

---

### Site Reliability Engineering: How Google Runs Production Systems (2016)

Beyer, Betsy, Chris Jones, Jennifer Petoff, and Niall Richard Murphy, eds. *Site Reliability Engineering: How Google Runs Production Systems*. Sebastopol, CA: O'Reilly Media, 2016.

- **ISBN**: 978-1-4919-2912-4 (paperback)
- **ISBN**: 978-1-4919-2911-7 (ebook)
- **Free online**: https://sre.google/sre-book/table-of-contents/

**Relevant Chapters**:

- **Chapter 17**: Testing for Reliability
- **Chapter 18**: Software Engineering in SRE
- **Chapter 28**: Accelerating SREs to On-Call and Beyond
- **Part IV**: Management (incident response, postmortems)

**Key Principle**:

> "Hope is not a strategy."

---

### Web Operations: Keeping the Data on Time (2010)

Allspaw, John, and Jesse Robbins, eds. *Web Operations: Keeping the Data on Time*. Sebastopol, CA: O'Reilly Media, 2010.

- **ISBN**: 978-1-4493-7744-1
- **Published**: June 21, 2010
- **O'Reilly**: https://www.oreilly.com/library/view/web-operations/9781449377465/

**Context**: Pre-dates the term "chaos engineering" but establishes the operational mindset. Contributors include pioneers who would go on to shape chaos engineering and DevOps.

**Notable Contributors**: Heather Champ, Richard Cook, Patrick Debois, Eric Ries, Theo Schlossnagle, Baron Schwartz, Andrew Shafer.

---

## Academic Fault Injection (Pre-Chaos)

### FIAT: Fault Injection Automated Testing (1990)

Barton, J.H., E.W. Czeck, Z.Z. Segall, and D.P. Siewiorek. "Fault Injection Experiments Using FIAT." *IEEE Transactions on Computers* 39, no. 4 (April 1990): 575-582.

- **DOI**: 10.1109/12.54842
- **Institution**: Carnegie Mellon University

**Context**: Academic foundation for software fault injection at Carnegie Mellon. D.P. Siewiorek's work established the theoretical framework that later tools would build upon.

---

### FERRARI: Fault and Error Automatic Real-time Injector (1992)

Kanawati, G.A., N.A. Kanawati, and J.A. Abraham. "FERRARI: A Flexible Software-Based Fault and Error Injection System." *IEEE Transactions on Computers* 44, no. 2 (February 1995): 248-260.

- **DOI**: 10.1109/12.364536
- **Conference**: First presented at 22nd International Symposium on Fault-Tolerant Computing (1992)

**Technique**: Software traps that inject errors into a system, activated by either a call to a specific memory location or a timeout.

---

### FTAPE: Fault Tolerance and Performance Evaluator (1994)

Tsai, Timothy K., and Ravishankar K. Iyer. "FTAPE: A Fault Injection Tool to Measure Fault Tolerance." In *Dependable Computing - EDCC-1*, Lecture Notes in Computer Science, vol. 852. Springer, 1994.

- **NASA Technical Report**: 19950018913
- **Archive**: https://archive.org/details/nasa_techdoc_19950018913
- **DOI**: 10.1007/BFb0024305

**Components**:
- System-wide fault injector
- Workload generator
- Workload activity measurement tool

**Capability**: Could inject faults into memory, registers, and disk accesses -- more comprehensive than earlier tools.

---

## Related Work

### Learning from Incidents

**Founder**: Nora Jones (2019)

**Purpose**: Open-sourcing and sharing learnings from incidents across organizations. Over 300 practitioners sharing new approaches to incident analysis.

**Key Insight** (from Nora Jones):

> "Engineers don't read postmortems more often because they're usually not written very well, they don't help them become better engineers, and it takes time to write them well -- time people don't always have."

---

### Principles of Chaos Engineering (USENIX SREcon17)

Rosenthal, Casey. "Principles of Chaos Engineering." USENIX SREcon17 Americas, San Francisco, March 2017.

- **URL**: https://www.usenix.org/conference/srecon17americas/program/presentation/rosenthal

**Context**: Conference talk that preceded the arXiv paper, presenting the principles to the SRE community.

---

# Alan Turing

**Core Contribution**: Mathematical foundations of computation, computability theory, artificial intelligence. The ACM Turing Award is named in his honor.

---

## On Computable Numbers (1936)

### Original Publication

Turing, Alan M. "On Computable Numbers, with an Application to the Entscheidungsproblem." *Proceedings of the London Mathematical Society*, Series 2, 42, no. 1 (1937): 230-265.

- **DOI**: [10.1112/plms/s2-42.1.230](https://doi.org/10.1112/plms/s2-42.1.230)
- **Received**: May 28, 1936
- **Read**: November 12, 1936
- **Published**: January 1, 1937
- **PDF**: [cs.virginia.edu](https://www.cs.virginia.edu/~robins/Turing_Paper_1936.pdf)

### The Turing Machine

The paper introduced the theoretical model now called the "Turing Machine" — an abstract computing device with an infinite tape and a read/write head that can perform fundamental computational operations.

> "The 'computable' numbers may be described briefly as the real numbers whose expressions as a decimal are calculable by finite means."

### The Entscheidungsproblem

Turing proved that no algorithm can determine whether an arbitrary mathematical statement is true or false — resolving Hilbert's Entscheidungsproblem negatively.

### The Halting Problem

The paper proved through diagonalization that it is impossible to construct a universal program that determines whether an arbitrary program will halt or loop indefinitely.

### Church-Turing Thesis

Turing's work established (independently of Alonzo Church) that all reasonable models of computation are equivalent in power.

---

## Computing Machinery and Intelligence (1950)

### Original Publication

Turing, Alan M. "I.—Computing Machinery and Intelligence." *Mind*, LIX (59), no. 236 (October 1950): 433-460.

- **DOI**: [10.1093/mind/LIX.236.433](https://doi.org/10.1093/mind/LIX.236.433)
- **Publisher**: Oxford University Press
- **Citations**: 6,000+

### The Opening Question

> "I propose to consider the question, 'Can machines think?' This should begin with definitions of the meaning of the terms 'machine' and 'think'. The definitions might be framed so as to reflect so far as possible the normal use of the words, but this attitude is dangerous."

### The Turing Test (Imitation Game)

Rather than asking "Can machines think?" (which he deemed ill-defined), Turing proposed an operational test: a judge communicates via text with two hidden entities (a human and a machine) and attempts to determine which is which.

### Nine Objections

Turing systematically addresses nine objections to machine thinking, including Lady Lovelace's Objection ("machines can only do what we program them to") and the Mathematical Objection (Gödel's incompleteness). His rebuttals remain philosophically relevant.

---

## Application to Architecture

1. **Decidability**: Some problems are undecidable — architectures cannot "solve" certain classes of problems
2. **Halting Problem in Practice**: Distributed systems inherit the halting problem — motivates timeouts, circuit breakers, graceful degradation
3. **Church-Turing Thesis**: All Turing-complete models are equivalent in *capability* — tradeoffs are about efficiency, observability, and resilience, not power
4. **Observable Behavior**: We cannot prove a component is "correct" internally; we can only verify observable behavior (contract-based testing, API versioning)

---

# Technology Strategy

Authoritative sources for economic and strategic thinking in software architecture. These inform **K**'s perspective: "Does this pay rent? Cathedral vs shed?"

---

## Conway's Law (1967/1968)

### Original Publication

Conway, Melvin E. "How Do Committees Invent?" *Datamation* 14, no. 4 (April 1968): 28-31.

- **URL**: [melconway.com](https://www.melconway.com/Home/Conways_Law.html)
- **Original Submission**: 1967 (rejected by Harvard Business Review)
- **Later Recognition**: Cited by Fred Brooks in *The Mythical Man-Month*

### The Principle

> "Organizations which design systems are constrained to produce designs which are copies of the communication structures of these organizations."

### Economic Insight

Organizational structure directly determines system architecture costs and flexibility. Teams cannot produce designs that contradict their communication patterns. This is not a guideline — it's a constraint.

---

## The Cathedral and the Bazaar (1997/1999)

### Original Publication

Raymond, Eric S. *The Cathedral and the Bazaar: Musings on Linux and Open Source by an Accidental Revolutionary*. Sebastopol, CA: O'Reilly Media, 1999.

- **ISBN**: 978-1-56592-724-7
- **Original Essay**: Presented at Linux Kongress, 1997
- **License**: Open Publication License v2.0
- **URL**: [catb.org](http://www.catb.org/~esr/writings/cathedral-bazaar/cathedral-bazaar/)

### Two Development Models

| Model | Characteristics |
|-------|-----------------|
| **Cathedral** | Centralized, planned releases, small core team |
| **Bazaar** | Distributed, continuous evolution, many contributors |

### Linus's Law

> "Given enough eyeballs, all bugs are shallow."

With enough reviewers, every problem is transparent to someone.

---

## Technical Debt (1992)

### Original Publication

Cunningham, Ward. "The WyCash Portfolio Management System." *OOPSLA '92 Experience Report*, Addendum to Proceedings, March 1992.

- **ACM DL**: [10.1145/157709.157715](https://doi.org/10.1145/157709.157715)
- **URL**: [c2.com](https://c2.com/doc/oopsla92.html)
- **Citations**: 799+

### The Original Metaphor

> "Shipping first-time code is like going into debt. A little debt speeds development so long as it is paid back promptly with a rewrite... Objects make the cost of this transaction tolerable. The danger occurs when the debt is not repaid. Every minute spent on not-quite-right code counts as interest on that debt."

### Common Misuse

Cunningham's metaphor was about *understanding* gaps, not *quality* gaps. He clarified in 2009: debt is code that reflects your understanding at the time, which later becomes outdated. "Sloppy code" isn't debt — it's just sloppy.

---

## Wardley Mapping (2005-2016)

### Origin

Wardley, Simon. *Wardley Maps* (book). Available free at [learnwardleymapping.com](https://learnwardleymapping.com/book/).

- **Creator**: Simon Wardley (developed at Fotango in 2005, refined at Canonical 2008-2010)
- **Primary Resources**: [wardleymaps.com](https://wardleymaps.com/), Medium series (2016)

### The Framework

Maps technology components along two axes:
- **Vertical (Y)**: Position in value chain (user need → underlying infrastructure)
- **Horizontal (X)**: Evolution stage (Genesis → Custom Build → Product → Commodity)

### Evolution Stages

| Stage | Characteristics | Build/Buy |
|-------|-----------------|-----------|
| **Genesis** | Novel, poorly understood, high uncertainty | Build (if core) |
| **Custom Build** | Bespoke solutions, emerging practices | Build |
| **Product** | Feature competition, best practices | Evaluate |
| **Commodity** | Utility, cost competition | Buy |

### Strategic Principle

Build vs buy decisions should be based on component *maturity* and *differentiation*. Commodities should be bought; differentiating components in early evolution stages should be built.

---

## Joel Spolsky on Rewrites (2000)

### Original Publication

Spolsky, Joel. "Things You Should Never Do, Part I." *Joel on Software*, April 6, 2000.

- **URL**: [joelonsoftware.com](https://www.joelonsoftware.com/2000/04/06/things-you-should-never-do-part-i/)

### The Netscape Case

Netscape rewrote their browser from 4.0 to 6.0. The rewrite took 3 years. During that time, competitors gained market share. The browser that shipped had bugs the old version had already fixed.

### The Argument

> "It's important to remember that when you start from scratch there is absolutely no reason to believe that you are going to do a better job than you did the first time."

Old code has accumulated bug fixes — each "ugly" line often represents a solved problem.

### Caveat for AI Era

This advice was written when code generation was expensive. The calculus changes when AI can rewrite quickly — but the *knowledge* embedded in old code remains valuable.

---

## Quality Economics (2019)

### Original Publication

Fowler, Martin. "Is High Quality Software Worth the Cost?" *martinfowler.com*, May 29, 2019.

- **URL**: [martinfowler.com](https://martinfowler.com/articles/is-quality-worth-cost.html)

### The Thesis

> "The 'cost' of high quality software is negative."

Higher internal quality reduces "cruft" (code that's hard to work with), which directly reduces development velocity. Quality investment pays for itself through faster feature development.

### Two Kinds of Quality

| Quality Type | Definition | Visible To |
|--------------|------------|------------|
| **External** | Features, UI, performance | Users |
| **Internal** | Code structure, maintainability | Developers |

Both matter economically. Internal quality compounds over time.

---

# Emerging Economics: AI and Software Development

**Status**: Rapidly consolidating (2024-2025). These are emerging patterns, not established wisdom. Publication dates indicate field maturity.

---

## Productivity Research

### GitHub Copilot Studies (2023-2024)

GitHub Blog. "Research: Quantifying GitHub Copilot's Impact on Developer Productivity and Happiness." 2024.

- **URL**: [github.blog](https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-on-developer-productivity-and-happiness/)

**Key Finding**: Treatment group completed tasks 55.8% faster (1h 11m vs 2h 41m).

**Caveat**: Microsoft research shows 11 weeks to fully realize benefits. Gains highest for routine tasks, not complex problem-solving.

### Anthropic Economic Index (2025)

Anthropic. "Anthropic Economic Index." February 2025.

- **URL**: [anthropic.com/economic-index](https://www.anthropic.com/economic-index)

> "Analysis of 100,000 Claude conversations finds AI reduces task time by 80% on average."

**Macroeconomic Projection**: If universally adopted over 10 years, current models could increase US labor productivity growth by 1.8% annually.

**Adoption Paradox**: 40% individual adoption vs 90% of firms report NOT using AI.

---

## The Build vs Buy Shift

### Multiple Sources (2024-2025)

- VentureBeat: "Build vs buy is dead — AI just killed it"
- Silicon Valley Product Group: "Build vs. Buy In The Age of AI"

**The Inversion**:

> "AI has made building accessible to everyone—what used to take weeks now takes hours, and what used to require fluency in a programming language now requires fluency in plain English."

**New Calculus**: Build for differentiated, integrated, fast-changing workflows. Buy for commodities.

**The CACE Principle**: "Changing Anything Changes Everything" — AI systems erode abstraction boundaries, creating entanglement.

---

## Technical Debt in AI Era

### MIT Sloan Management Review (2024-2025)

"How to Manage Tech Debt in the AI Era." *MIT Sloan Management Review*.

- **URL**: [sloanreview.mit.edu](https://sloanreview.mit.edu/article/how-to-manage-tech-debt-in-the-ai-era/)

**Counterintuitive Finding**:

> "AI has significantly increased the real cost of carrying tech debt, as generative AI dramatically widens the gap in velocity between low-debt and high-debt coding."

Clean codebases compound with AI adoption. Messy codebases compound against you.

---

## Disposable Software Economics

### The One-Shot App Phenomenon

Multiple sources (2024-2025):
- Code Conductor: "Disposable AI Apps"
- UBOS: "The Rise of Disposable Code"

**Definition**: Lightweight, single-purpose applications built rapidly for immediate use, then discarded.

**Jevons' Paradox Applied**: As production cost decreases, consumption increases. Lower development costs → explosion of single-use software.

---

## Emerging Principles

### What's Changing

| Old Assumption | AI Challenge |
|----------------|--------------|
| Skill gaps require training | Capability bridging through tools |
| Experience flattens with tools | Junior devs need fundamentals to benefit |
| Technical debt is sunk cost | Debt is now competitive liability |
| Design precedes coding | Design emerges from iteration |
| Reusable software is always better | Disposable software is economically rational |

### What's Timeless

- Trade-offs exist — no free lunch
- Conway's Law — org structure constrains design
- Essential complexity cannot be eliminated, only organized
- Computability limits remain (Turing)
- Economic incentives drive behavior

---

## Verification Notes

All citations verified against:

1. **ACM Digital Library** (DOI links tested)
2. **Dijkstra Archive at UT Austin** (EWD transcriptions)
3. **Microsoft Research** (Lamport papers, Ramalingam/Vaswani paper)
4. **ScienceDirect** (Zadeh paper)
5. **Publisher records** (Taleb, Chesterton, Hunt & Thomas, Brooks, Meyer, Richardson, Raymond)
6. **Quote Investigator** (Alan Kay quote origins)
7. **Cornell CS Archive** (Sagas paper PDF)
8. **UCI ICS** (Helland paper PDF)
9. **Martin Fowler's website** (Event Sourcing, CQRS articles, Quality Economics)
10. **microservices.io** (Richardson patterns)
11. **arXiv.org** (Chaos Engineering paper)
12. **Netflix Tech Blog** (original Simian Army posts)
13. **IEEE Xplore** (academic fault injection papers)
14. **USENIX Archives** (conference presentations)
15. **GitHub** (Netflix open source releases, Copilot research)
16. **Proceedings of London Mathematical Society** (Turing 1936)
17. **Oxford Academic / Mind Journal** (Turing 1950)
18. **Datamation archives** (Conway's Law)
19. **c2.com** (Ward Cunningham, Technical Debt)
20. **Joel on Software** (Spolsky strategy articles)
21. **Anthropic Economic Index** (Claude usage analysis)
22. **MIT Sloan Management Review** (Technical debt in AI era)
23. **VentureBeat, SVPG** (Build vs Buy analysis)
24. **Wardley Maps community** (learnwardleymapping.com)

Last verified: 2026-01-18
