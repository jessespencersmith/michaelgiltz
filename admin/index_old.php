<?php
/**
 * Michael Giltz Website Admin Panel
 * Simple interface for updating the website
 */

// Get last update time
$last_update_file = '../logs/last_update.txt';
$last_update = file_exists($last_update_file) ? file_get_contents($last_update_file) : 'Never';

// Handle update request
$message = '';
$message_type = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action'])) {
    if ($_POST['action'] === 'update') {
        // Run the Python script
        $output = array();
        $return_var = 0;
        
        // Change to parent directory
        chdir('..');
        
        // Try different Python commands
        $python_cmds = array('python3', 'python', '/usr/bin/python3', '/usr/bin/python');
        $success = false;
        
        foreach ($python_cmds as $python) {
            exec("$python scripts/process_pdfs.py 2>&1", $output, $return_var);
            if ($return_var === 0) {
                $success = true;
                break;
            }
        }
        
        if ($success) {
            $message = "Website updated successfully!";
            $message_type = 'success';
            $last_update = date('Y-m-d H:i:s');
        } else {
            $message = "Error updating website: " . implode("\n", $output);
            $message_type = 'error';
        }
    } elseif ($_POST['action'] === 'test') {
        // Run test mode
        chdir('..');
        exec("python scripts/process_pdfs.py --test 2>&1", $output, $return_var);
        
        if ($return_var === 0) {
            $message = "Test completed successfully! Processed 5 PDFs.";
            $message_type = 'success';
        } else {
            $message = "Test failed: " . implode("\n", $output);
            $message_type = 'error';
        }
    }
}

// Get recent PDFs
$recent_pdfs = array();
$scan_dir = '../scans';
if (is_dir($scan_dir)) {
    $files = glob($scan_dir . '/*.pdf');
    usort($files, function($a, $b) {
        return filemtime($b) - filemtime($a);
    });
    $recent_pdfs = array_slice($files, 0, 10);
}

// Get processing log
$log_file = '../logs/processing.log';
$recent_log = '';
if (file_exists($log_file)) {
    $lines = file($log_file);
    $recent_log = implode('', array_slice($lines, -20));
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Michael Giltz Website Admin</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background-color: #333;
            color: white;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 30px;
        }
        .header h1 {
            margin: 0;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .update-section {
            text-align: center;
            margin-bottom: 40px;
            padding: 30px;
            background-color: #f9f9f9;
            border-radius: 5px;
        }
        .btn {
            display: inline-block;
            padding: 15px 40px;
            font-size: 18px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            margin: 10px;
        }
        .btn-primary {
            background-color: #007bff;
            color: white;
        }
        .btn-primary:hover {
            background-color: #0056b3;
        }
        .btn-secondary {
            background-color: #6c757d;
            color: white;
        }
        .btn-secondary:hover {
            background-color: #545b62;
        }
        .info-box {
            background-color: #e9ecef;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .message {
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .message.success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .message.error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .recent-files {
            margin-top: 30px;
        }
        .file-list {
            list-style: none;
            padding: 0;
        }
        .file-list li {
            padding: 10px;
            border-bottom: 1px solid #eee;
        }
        .file-list li:hover {
            background-color: #f9f9f9;
        }
        .log-section {
            margin-top: 30px;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 5px;
        }
        .log-content {
            background-color: #fff;
            border: 1px solid #dee2e6;
            padding: 15px;
            font-family: monospace;
            font-size: 12px;
            max-height: 300px;
            overflow-y: auto;
        }
        .stats {
            display: flex;
            justify-content: space-around;
            margin: 30px 0;
        }
        .stat-box {
            text-align: center;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 5px;
            flex: 1;
            margin: 0 10px;
        }
        .stat-number {
            font-size: 36px;
            font-weight: bold;
            color: #007bff;
        }
        .stat-label {
            color: #6c757d;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Michael Giltz Website Admin</h1>
        <p>Manage and update your website content</p>
    </div>

    <div class="container">
        <?php if ($message): ?>
            <div class="message <?php echo $message_type; ?>">
                <?php echo htmlspecialchars($message); ?>
            </div>
        <?php endif; ?>

        <div class="info-box">
            <strong>Last Update:</strong> <?php echo htmlspecialchars($last_update); ?>
        </div>

        <div class="update-section">
            <h2>Update Website</h2>
            <p>Click the button below to process all PDFs and update the website.</p>
            
            <form method="post" style="display: inline;">
                <input type="hidden" name="action" value="update">
                <button type="submit" class="btn btn-primary">
                    Update Website Now
                </button>
            </form>
            
            <form method="post" style="display: inline;">
                <input type="hidden" name="action" value="test">
                <button type="submit" class="btn btn-secondary">
                    Run Test (5 PDFs)
                </button>
            </form>
        </div>

        <div class="stats">
            <div class="stat-box">
                <div class="stat-number"><?php echo count(glob('../scans/*.pdf')); ?></div>
                <div class="stat-label">Total PDFs</div>
            </div>
            <div class="stat-box">
                <div class="stat-number"><?php echo count(glob('../extracted_content/*.html')); ?></div>
                <div class="stat-label">Extracted HTML</div>
            </div>
            <div class="stat-box">
                <div class="stat-number"><?php echo count(glob('../*.htm')); ?></div>
                <div class="stat-label">HTML Pages</div>
            </div>
        </div>

        <div class="recent-files">
            <h3>Recently Added PDFs</h3>
            <?php if (empty($recent_pdfs)): ?>
                <p>No PDFs found.</p>
            <?php else: ?>
                <ul class="file-list">
                    <?php foreach ($recent_pdfs as $pdf): ?>
                        <?php 
                        $filename = basename($pdf);
                        $modified = date('Y-m-d H:i:s', filemtime($pdf));
                        ?>
                        <li>
                            <strong><?php echo htmlspecialchars($filename); ?></strong><br>
                            <small>Modified: <?php echo $modified; ?></small>
                        </li>
                    <?php endforeach; ?>
                </ul>
            <?php endif; ?>
        </div>

        <div class="info-box" style="margin-top: 30px;">
            <h3>Quick Instructions</h3>
            <ol>
                <li>Upload your PDFs to the server as usual</li>
                <li>Click "Update Website Now" to process all new PDFs</li>
                <li>The website will automatically update with new content</li>
                <li>Use "Run Test" to test with just 5 PDFs first</li>
            </ol>
        </div>

        <?php if ($recent_log): ?>
        <div class="log-section">
            <h3>Recent Processing Log</h3>
            <div class="log-content">
                <pre><?php echo htmlspecialchars($recent_log); ?></pre>
            </div>
        </div>
        <?php endif; ?>
    </div>

    <div style="text-align: center; margin-top: 30px; color: #666;">
        <p>&copy; <?php echo date('Y'); ?> Michael Giltz. All rights reserved.</p>
    </div>
</body>
</html>