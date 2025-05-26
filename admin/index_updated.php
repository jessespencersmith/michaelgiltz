<?php
/**
 * Michael Giltz Website Admin Panel - Updated for Combined Pages
 * Simple interface for updating the website with new combined HTML pages
 */

// Get last update time
$last_update_file = '../logs/last_update.txt';
$last_update = file_exists($last_update_file) ? file_get_contents($last_update_file) : 'Never';

// Handle update request
$message = '';
$message_type = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action'])) {
    if ($_POST['action'] === 'update') {
        // Run the new Python script for combined pages
        $output = array();
        $return_var = 0;
        
        // Change to parent directory
        chdir('..');
        
        // Try different Python commands
        $python_cmds = array('python3', 'python', '/usr/bin/python3', '/usr/bin/python');
        $success = false;
        
        foreach ($python_cmds as $python) {
            exec("$python scripts/process_new_pdfs.py 2>&1", $output, $return_var);
            if ($return_var === 0) {
                $success = true;
                break;
            }
        }
        
        if ($success) {
            $message = "Website updated successfully! New articles have been processed.";
            $message_type = 'success';
            $last_update = date('Y-m-d H:i:s');
        } else {
            $message = "Error updating website: " . implode("\n", $output);
            $message_type = 'error';
        }
    } elseif ($_POST['action'] === 'test') {
        // Run test mode
        chdir('..');
        exec("python3 scripts/process_new_pdfs.py --test 2>&1", $output, $return_var);
        
        if ($return_var === 0) {
            $message = "Test completed successfully! Processed 1 PDF.";
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

// Check for unprocessed PDFs
$processed_file = '../logs/processed_pdfs.json';
$processed_pdfs = array();
if (file_exists($processed_file)) {
    $processed_pdfs = json_decode(file_get_contents($processed_file), true);
}

$all_pdfs = array_map('basename', glob($scan_dir . '/*.pdf'));
$unprocessed_count = count(array_diff($all_pdfs, $processed_pdfs));

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
    <title>Michael Giltz Website Admin - Combined Pages</title>
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
        .warning-box {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
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
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .file-list li:hover {
            background-color: #f9f9f9;
        }
        .status-badge {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: bold;
        }
        .status-processed {
            background-color: #28a745;
            color: white;
        }
        .status-unprocessed {
            background-color: #dc3545;
            color: white;
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
        .new-feature {
            background-color: #e7f3ff;
            border: 1px solid #b3d9ff;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .new-feature h3 {
            margin-top: 0;
            color: #004085;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Michael Giltz Website Admin</h1>
        <p>Combined PDF + Text Pages Management</p>
    </div>

    <div class="container">
        <?php if ($message): ?>
            <div class="message <?php echo $message_type; ?>">
                <?php echo htmlspecialchars($message); ?>
            </div>
        <?php endif; ?>

        <div class="new-feature">
            <h3>🆕 New Combined Pages System</h3>
            <p>The website now uses combined HTML pages that include both the PDF viewer and extracted text for better SEO and user experience.</p>
        </div>

        <div class="info-box">
            <strong>Last Update:</strong> <?php echo htmlspecialchars($last_update); ?>
        </div>

        <?php if ($unprocessed_count > 0): ?>
        <div class="warning-box">
            <strong>⚠️ Unprocessed PDFs:</strong> There are <?php echo $unprocessed_count; ?> PDFs that need processing.
        </div>
        <?php endif; ?>

        <div class="update-section">
            <h2>Process New Articles</h2>
            <p>Click the button below to create combined HTML pages for all new PDFs.</p>
            
            <form method="post" style="display: inline;">
                <input type="hidden" name="action" value="update">
                <button type="submit" class="btn btn-primary">
                    Process New PDFs
                </button>
            </form>
            
            <form method="post" style="display: inline;">
                <input type="hidden" name="action" value="test">
                <button type="submit" class="btn btn-secondary">
                    Test Mode (1 PDF)
                </button>
            </form>
        </div>

        <div class="stats">
            <div class="stat-box">
                <div class="stat-number"><?php echo count(glob('../scans/*.pdf')); ?></div>
                <div class="stat-label">Total PDFs</div>
            </div>
            <div class="stat-box">
                <div class="stat-number"><?php echo count(glob('../articles/*.html')); ?></div>
                <div class="stat-label">Combined Pages</div>
            </div>
            <div class="stat-box">
                <div class="stat-number"><?php echo $unprocessed_count; ?></div>
                <div class="stat-label">Need Processing</div>
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
                        $is_processed = in_array($filename, $processed_pdfs);
                        ?>
                        <li>
                            <div>
                                <strong><?php echo htmlspecialchars($filename); ?></strong><br>
                                <small>Modified: <?php echo $modified; ?></small>
                            </div>
                            <span class="status-badge <?php echo $is_processed ? 'status-processed' : 'status-unprocessed'; ?>">
                                <?php echo $is_processed ? 'Processed' : 'Unprocessed'; ?>
                            </span>
                        </li>
                    <?php endforeach; ?>
                </ul>
            <?php endif; ?>
        </div>

        <div class="info-box" style="margin-top: 30px;">
            <h3>📋 How the New System Works</h3>
            <ol>
                <li><strong>Upload PDFs</strong> to the <code>scans/</code> folder via FTP as usual</li>
                <li><strong>Click "Process New PDFs"</strong> to create combined HTML pages</li>
                <li><strong>Each PDF gets an HTML page</strong> with:
                    <ul>
                        <li>Embedded PDF viewer at the top</li>
                        <li>Extracted text content for SEO</li>
                        <li>Navigation back to the main site</li>
                    </ul>
                </li>
                <li><strong>Publication pages are automatically updated</strong> with links to new articles</li>
            </ol>
            
            <h4>Important Notes:</h4>
            <ul>
                <li>PDFs must follow the naming format: <code>Publication-Title-MM-DD-YYYY.pdf</code></li>
                <li>Processing extracts text from PDFs for search engine indexing</li>
                <li>The original PDFs remain in place and are embedded in the HTML pages</li>
            </ul>
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