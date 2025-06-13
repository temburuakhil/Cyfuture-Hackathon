const axios = require('axios');
const cron = require('node-cron');

const services = [
  {
    name: 'Main App',
    url: 'https://cyfuture-hackathon.vercel.app'
  },
  {
    name: 'Finbot AI',
    url: 'https://finbot-linguist-ai.onrender.com/health'
  },
  {
    name: 'GST Assistant',
    url: 'https://gst-assistant.onrender.com/health'
  },
  {
    name: 'Invoice Processor',
    url: 'https://invoice-processor.onrender.com/health'
  }
];

async function checkHealth() {
  console.log(`\nHealth Check - ${new Date().toISOString()}`);
  console.log('-'.repeat(50));

  for (const service of services) {
    try {
      const start = Date.now();
      const response = await axios.get(service.url);
      const duration = Date.now() - start;

      console.log(`${service.name}:`);
      console.log(`  Status: ${response.status === 200 ? '✅ Healthy' : '❌ Unhealthy'}`);
      console.log(`  Response Time: ${duration}ms`);
    } catch (error) {
      console.log(`${service.name}:`);
      console.log('  Status: ❌ Error');
      console.log(`  Error: ${error.message}`);
    }
  }
}

// Run health check every 5 minutes
cron.schedule('*/5 * * * *', checkHealth);

// Initial check
checkHealth();
