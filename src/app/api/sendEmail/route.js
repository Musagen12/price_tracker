// /src/app/api/sendEmail/route.js

import nodemailer from 'nodemailer';

export async function POST(request) {
  console.log('API Handler Invoked'); // Debugging log
  try {
    const { email, targetPrice } = await request.json();
    console.log(`Received email: ${email}, targetPrice: ${targetPrice}`); // Debugging log

    // Create a transporter object using Gmail SMTP
    const transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: process.env.EMAIL_USER, // Email stored in environment variable
        pass: process.env.EMAIL_PASS, // Email password stored securely (App Password)
      },
    });

    // Set the mail options
    const mailOptions = {
      from: process.env.EMAIL_USER, // Sender address
      to: email, // Receiver email from the form
      subject: 'Target Price Notification',
      text: `Your target price has been set at $${targetPrice}.`, // Plain text body
    };

    // Send the email
    await transporter.sendMail(mailOptions);
    console.log('Email sent successfully'); // Debugging log

    // Always send back a JSON response
    return new Response(JSON.stringify({ message: 'Email sent successfully!' }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (error) {
    console.error('Error sending email:', error);
    return new Response(JSON.stringify({ error: 'Failed to send email' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}
