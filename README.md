# pyImguiOs

This is likely to be rewritten using a different set of GUI bindings, which is
fine as I didn't get very far anyway. Kept for historical reasons.

I'll likely be developing an object-oriented interface on top of the DearPyGui
bindings, to try and provide a retained-mode interface to imgui (better
performance) that is still very easy to use. A new "toy oeprating system" will
be developed on top of that.

### A toy "operating system" written using python and imgui.

Inspired by "fantasy consoles" like the pico8, pyImguiOs is a fantasy operating
system. It's not intended for serious use, rather it's intended to be fun to use
and allow for the very fast development of simple GUI apps.

pyImguiOs is of course just a program that runs on top of linux, like your web
browser or the android operating system. We make use of linux function calls and
linux programs. It is intended to be a fully self-contained "operating system"
though.

PyImguiOs is a single-process cooperative-multitasking "os". This has some
significant drawbacks, a `sleep(100)` call in the wrong place will freeze the
entire system. It also makes it very hard to scale, since all programs need to
run on one CPU. A heavy program that legitimatly uses a lot of resources will
bring the whole system to a crawl. It's also impossible to do any sort of
isolation/sandboxing/privilege-separation.

These issues would be fixable with a big enough budget, talk to me about
network-transparent object proxying, capability-based security, how how to
actually make that all performant.

Imgui is by far the easiest GUI framework I've ever used, at least for simple
UIs. We want to keep UIs simple enough to be easy to implement.

The major advantage is that everything is an object. This makes scripting very
easy. The unix philosophy of "everything is a file" has held up very well, I'd
like to see how well "everything is a python object" works.

Historically unix philosophy does not work well with GUI apps, it's my hope that
this "everything is a python object" system is largely compatible with the rest
of unix philosophy, simple and introspectable enough that it's not a huge
downgrade from text streams (except in terms of performance, where I expect text
streams to remain king), and flexible enough that you can implement a
complicated program as a series of small components that do one thing and do it well,
even if you have to deal with signaling, GUI callbacks, and all the other 
complexities that come with writing a GUI program.
