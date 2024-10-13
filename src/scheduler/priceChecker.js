import 'dotenv/config';
import { MailerSend, EmailParams, Sender, Recipient } from 'mailersend';

const mailerSend = new MailerSend({
    apiKey: process.env.MAILERSEND_API_KEY,
});

const sentFrom = new Sender("MS_k9qFH7@trial-0r83ql3563v4zw1j.mlsender.net", "Price Tracker");

// Function to send the email notification with product details
export const sendEmailNotification = async (recipientEmail, productId, targetPrice, currentPrice) => {
    const recipients = [new Recipient(recipientEmail, 'Price Tracker User')];

    const message = `
        Price target reached for product ID: ${productId}.
        Target Price: $${targetPrice}.
        Current Price: $${currentPrice}.
    `;

    const emailParams = new EmailParams()
        .setFrom(sentFrom)
        .setTo(recipients)
        .setReplyTo(sentFrom)
        .setSubject('Price Drop Alert!')
        .setHtml(`<strong>${message}</strong>`)
        .setText(message);

    try {
        await mailerSend.email.send(emailParams);
        console.log(`Email sent successfully to ${recipientEmail} for product ID: ${productId}.`);
    } catch (error) {
        console.error('Failed to send email:', error);
    }
};
