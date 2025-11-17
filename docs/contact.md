---
layout: page
title: Contact
permalink: /contact/
---

If you would like to reach out or share ideas, you can send a message below.  
I read every submission — please include your email if you would like a reply.

<form class="contact-form" action="https://formspree.io/f/mvgdjrqq" method="POST">
  <label>
    Your name
    <input type="text" name="name" required>
  </label>

  <label>
    Your email
    <input type="email" name="_replyto" required>
  </label>

  <label>
    Message
    <textarea name="message" rows="6" required></textarea>
  </label>

  <!-- Optional honeypot field to trap bots -->
  <input type="text" name="_gotcha" style="display:none">

  <button type="submit" class="btn">Send</button>
</form>

<input type="hidden" name="_redirect" value="{{ '/thanks/' | relative_url }}">

