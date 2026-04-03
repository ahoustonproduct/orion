const { execSync } = require('child_process');
const os = require('os');
const fs = require('fs');

class OrionTools {
  static openApp(appName) {
    try {
      const platform = os.platform();
      let cmd;
      if (platform === 'darwin') {
        cmd = `open -n -a "${appName}"`; // MacOS
      } else if (platform === 'win32') {
        // Windows start command
        cmd = `start "" "${appName}"`;
      } else if (platform === 'linux') {
        cmd = `xdg-open "${appName}"`;
      } else {
        return `Unsupported OS: ${platform}`;
      }
      
      execSync(cmd, { stdio: 'ignore' });
      return `Successfully launched ${appName}.`;
    } catch (error) {
      return `Failed to open ${appName}: ${error.message}. Make sure the app name is correct and accessible via shell.`;
    }
  }

  static getSystemStatus() {
    try {
      const freeMem = (os.freemem() / 1024 / 1024 / 1024).toFixed(2);
      const totalMem = (os.totalmem() / 1024 / 1024 / 1024).toFixed(2);
      const cpuLoad = os.loadavg()[0].toFixed(2); // 1-minute load avg
      const platform = os.platform();
      const release = os.release();

      return `OS: ${platform} ${release} | CPU Load (1m): ${cpuLoad} | RAM: ${freeMem}GB free of ${totalMem}GB`;
    } catch (error) {
      return `Failed to get system status: ${error.message}`;
    }
  }

  static listDirectory() {
    try {
      const cwd = process.cwd();
      const files = fs.readdirSync(cwd);
      return `Target directory: ${cwd}\nContents:\n${files.join(', ')}`;
    } catch (error) {
      return `Failed to list directory: ${error.message}`;
    }
  }
}

module.exports = OrionTools;
