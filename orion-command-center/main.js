const { OpenAI } = require('openai');
const readline = require('readline/promises');
const config = require('./config');
const memory = require('./memory');
const OrionTools = require('./tools');

const openai = new OpenAI({
  baseURL: config.OLLAMA_URL,
  apiKey: "ollama" // Required by library, ignored by Ollama
});

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

async function mainLoop() {
  console.log(`\n================================`);
  console.log(` Orion AI Command Center (Node.js) `);
  console.log(`================================`);
  console.log(`Model: ${config.MODEL_NAME}`);
  console.log(`OS Preference: ${config.USER_PROFILE.osPreference}`);
  console.log(`Type 'exit' to quit.\n`);

  let memoryContext = await memory.getAllContext();
  
  let systemPrompt = `You are Orion, a System Assistant. 
You have access to tools to open apps and check system status. You have a persistent memory.
If a user asks you to remember something, use the MEMORY tool by outputting ONLY: MEMORY: <key> | <value>
If a user asks to perform a system action, use the TOOL tool by outputting ONLY: TOOL: <tool_name> | <argument>
Available tools: openApp, getSystemStatus, listDirectory.
For example, to open Safari: TOOL: openApp | Safari
To save a memory: MEMORY: favoriteColor | blue
If it's just a general chat, reply normally. Be concise and efficient.
Here is your current memory context:
${memoryContext}`;

  let messages = [
    { role: "system", content: systemPrompt }
  ];

  while (true) {
    const input = await rl.question("User: ");
    
    if (input.toLowerCase() === 'exit' || input.toLowerCase() === 'quit') {
      rl.close();
      break;
    }

    messages.push({ role: "user", content: input });

    try {
      const response = await openai.chat.completions.create({
        model: config.MODEL_NAME,
        messages: messages,
        temperature: 0.1
      });

      const reply = response.choices[0].message.content.trim();
      
      let finalReply = reply;
      let handled = false;

      // Intent parsing
      if (reply.includes("MEMORY:")) {
        const match = reply.match(/MEMORY:\s*(.+)\s*\|\s*(.+)/);
        if (match) {
          const key = match[1].trim();
          const value = match[2].trim();
          await memory.save(key, value);
          finalReply = `I have updated my memory: ${key} = ${value}.`;
          
          // Update the system prompt with new memory
          memoryContext = await memory.getAllContext();
          messages[0].content = systemPrompt.split("Here is your current memory context:\n")[0] + "\nHere is your current memory context:\n" + memoryContext;
          
          console.log(`Orion [Memory Updated]: ${finalReply}`);
          handled = true;
        }
      } 
      
      if (!handled && reply.includes("TOOL:")) {
        const match = reply.match(/TOOL:\s*([a-zA-Z]+)\s*\|?\s*(.*)/);
        if (match) {
          const toolName = match[1].trim();
          const toolArg = match[2] ? match[2].trim() : "";
          
          let result = "";
          if (toolName === "openApp") {
            // Guardrail confirmation
            const confirm = await rl.question(`Orion wants to open '${toolArg}'. Allow? (y/n): `);
            if (confirm.toLowerCase() === 'y' || confirm.toLowerCase() === 'yes') {
              result = OrionTools.openApp(toolArg);
            } else {
              result = "User cancelled app launch.";
            }
          } else if (toolName === "getSystemStatus") {
            result = OrionTools.getSystemStatus();
          } else if (toolName === "listDirectory") {
            result = OrionTools.listDirectory();
          } else {
            result = `Unknown tool requested: ${toolName}`;
          }
          
          console.log(`Orion [Tool Execution]: ${result}`);
          
          // Optionally, feed the result back to the LLM to formulate a response
          messages.push({ role: "assistant", content: reply });
          messages.push({ role: "system", content: `Tool execution result: ${result}`});
          handled = true;
        }
      }

      if (!handled) {
        console.log(`Orion: ${reply}`);
        messages.push({ role: "assistant", content: reply });
      }

    } catch (error) {
      if (error.code === 'ECONNREFUSED') {
        console.error(`[Error] Could not connect to Ollama at ${config.OLLAMA_URL}. Make sure Ollama is running.`);
      } else {
        console.error(`[Error] ${error.message}`);
      }
    }
  }
}

mainLoop();
