// /src/app/api/sendEmail/route.js
import 'dotenv/config';
import { MailerSend, EmailParams, Sender, Recipient } from "mailersend";
import { addPriceCheck } from '../../../db/db'; // Import your database function

export async function POST(request) {
  try {
    const { email, targetPrice, productId } = await request.json();  // Get productId
    if (!email || !targetPrice || !productId) {  // Validate productId
      throw new Error('Email, targetPrice, and productId are required.');
    }

    // Save the email, targetPrice, and productId to the database
    addPriceCheck(email, targetPrice, productId);

    // Proceed with sending the email as before...
    const mailerSend = new MailerSend({ apiKey: process.env.MAILERSEND_API_KEY });
    const sentFrom = new Sender("MS_k9qFH7@trial-0r83ql3563v4zw1j.mlsender.net", "Price Tracker");
    const recipients = [new Recipient(email, "Your Client")];

    const personalization = [{
      email: email,
      data: {
        email: email,
        product_id: productId,  // Include productId in email data
        targetPrice: targetPrice
      }
    }];

    const emailParams = new EmailParams()
      .setFrom(sentFrom)
      .setTo(recipients)
      .setReplyTo(sentFrom)
      .setSubject("Target Price Notification")
      .setTemplateId('z86org8797elew13')
      .setPersonalization(personalization);
    
    await mailerSend.email.send(emailParams);
    
    return new Response(JSON.stringify({ message: 'Email sent successfully!' }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (error) {
    console.error('Error sending email:', error.message || error);
    return new Response(
      JSON.stringify({ error: 'Failed to send email: ' + (error.message || 'Unknown error') }),
      {
        status: 500,
        headers: { 'Content-Type': 'application/json' },
      }
    );
  }
}
