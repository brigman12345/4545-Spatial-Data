# Data Manager

I wanted to do something with an Armageddon theme using a bunch of geojson files when I found myself solving the issue of too much data, and how do I display so much data seamlessly on a map?

The mapping libraries we are using were doing ok with the data, but not awesome, and I found that I wanted to handle the loading myself. This triggered the wise old question: "Really Terry? Implement all of it? Like ... ALL OF IT?" Then I remembered being scarred during my PhD dissertation. This assignment is so you don't get emotionally scarred like I did.

The assignment shows you how to go from implementing, learning, and understanding to _power using libraries like a boss_.

## 🧠 Build vs Borrow — Read This Before You Import Another Library

Let me talk to you like a future developer, not just a student grinding through assignments.

You are learning computer science, which means you are learning how systems work—not just how to use them. At the same time, you are not being trained to rebuild the entire modern software ecosystem from scratch every time you sit down to write code.

So where’s the line?

That’s what this handout is about.

---

# ⚖️ The Two Bad Extremes

There are two traps students fall into.

The first is what I call **library worship**:

> “There’s a package for it, so I must understand it.”

You don’t. You installed something and got a result. That’s not understanding—that’s outsourcing.

The second is **from-scratch purism**:

> “Real programmers implement everything themselves.”

Also wrong. That mindset leads to wasted time, fragile code, and solving problems that have already been solved better by people who have spent years refining those solutions.

The goal is not to live at either extreme.

---

# 🎯 The Skill That Actually Matters

> **Understand enough to judge the abstraction.**

That means:

- You know what a tool is doing conceptually
- You know what assumptions it makes
- You can tell when it’s the wrong tool
- You can debug when things go wrong

That’s the difference between someone who _uses_ tools and someone who _understands_ them.

---

# 🧱 Why We Build Things From Scratch (Yes, There’s a Point)

You’ve probably wondered:

> “Why are we writing our own linked list when C++ already has vectors and deques?”

Fair question.

Here’s why.

---

## Example 1 — Linked Lists vs Vectors

When you build a linked list yourself, you are forced to confront things that a vector hides:

- What actually happens when you insert something in the middle?
- Why does a vector sometimes have to shift half its elements?
- What is the cost of resizing?
- What does “O(1) insertion” actually mean in practice?

A `std::vector` makes everything look easy:

```cpp
v.insert(v.begin() + i, value);
```

But under the hood:

- memory might be reallocated
- elements might be copied or moved
- performance depends on capacity

When you’ve written a linked list yourself, you _feel_ the difference between:

- pointer rewiring (cheap)
- shifting memory (expensive)

Without that experience, Big-O is just a slogan.

---

## Example 2 — Queue vs Deque

When you implement a queue from scratch, especially using an array, you run into real problems:

- What happens when you reach the end of the array?
- Do you shift everything left? (slow)
- Do you wrap around? (circular buffer)
- How do you track front and rear correctly?

Now when you use:

```cpp
std::deque<int> q;
```

You understand:

- why it exists
- why it’s not just a vector
- what problem it solves

Without building a queue yourself, a deque is just “some container that works.”  
Afterward, it becomes a deliberate choice.

---

# 🧩 The Right Way to Learn This

Here’s the approach that actually builds skill.

First, you build a small version yourself. Not perfect, not optimized, just functional. You struggle a little. You see where things break. You understand the moving parts.

Then, you use the real tool. Now you’re not blindly trusting it—you’re recognizing what it’s doing for you.

And most importantly, you never let a library replace thinking. If something looks off, you question it. If performance seems wrong, you investigate. You’re not guessing—you’re reasoning.

---

# 🧠 A Simple Reality Check

If you can’t build a small version of something, you probably don’t understand it.

If you insist on building the full version of everything, you probably don’t understand engineering.

Both matter.

---

# 🚂 Why This Matters for the Data Project

This project is not about drawing train tracks on a map. It’s about learning how to think like someone who builds systems that deal with real data.

You’re working with a large GeoJSON file—large enough that naïvely loading and rendering it becomes inefficient or outright impractical. That forces you into a situation where you have to think.

You’ll start by writing your own simplification logic. It won’t be perfect, and that’s exactly the point. You’ll see how reducing detail affects shape. You’ll notice how performance improves as complexity drops. You’ll begin to understand the relationship between data size and usability.

Then you’ll introduce multiple levels of detail. Instead of treating the dataset as one monolithic object, you’ll create versions of it that are appropriate for different zoom levels. Now you’re not just processing data—you’re making decisions about _when_ and _how much_ data should be used.

You’ll implement logic that switches between these layers depending on what the user is looking at. That’s a fundamental idea in spatial systems: don’t process what you don’t need.

At some point, it will become obvious that doing all of this manually for a full-scale system would be painful, error-prone, and inefficient. That realization is not failure—that’s the lesson.

Now when you are shown professional tools—vector tiling systems, optimized spatial libraries, rendering engines—you will understand _why they exist_. Not because someone told you, but because you experienced the problem they solve.

That’s the difference between:

- memorizing tools
- and understanding systems

---

# 💬 The One Sentence You Should Remember

> **Build the smallest version that teaches the idea. Borrow the version that survives the real world.**

If you carry that with you, you’ll avoid a lot of wasted time—and you’ll make much better technical decisions than most people starting out.

---

# 🚀 Final Thought

You are not being trained to be a passive consumer of libraries.

You are being trained to:

- understand what’s happening
- make informed decisions
- and build when it matters

That’s real computer science.

Now go build something smart… and stop trying to rebuild the internet while you’re at it.
