<?php
/**
 * Simple search functionality for Michael Giltz website
 * Searches through extracted HTML content
 */

$search_query = isset($_GET['q']) ? trim($_GET['q']) : '';
$results = array();

if ($search_query && strlen($search_query) >= 3) {
    $extracted_dir = 'extracted_content';
    $max_results = 50;
    
    // Search through HTML files
    $files = glob($extracted_dir . '/*.html');
    
    foreach ($files as $file) {
        $content = file_get_contents($file);
        $filename = basename($file);
        
        // Remove HTML tags for searching
        $text = strip_tags($content);
        
        // Case-insensitive search
        if (stripos($text, $search_query) !== false) {
            // Extract title from filename
            preg_match('/^(.+?)-(.+?)-(\d+)-(\d+)-(\d+)\.html$/', $filename, $matches);
            if ($matches) {
                $publication = $matches[1];
                $title = str_replace('_', ' ', $matches[2]);
                $date = $matches[3] . '-' . $matches[4] . '-' . $matches[5];
                
                // Get excerpt around the search term
                $pos = stripos($text, $search_query);
                $start = max(0, $pos - 100);
                $excerpt = substr($text, $start, 200);
                $excerpt = '...' . trim($excerpt) . '...';
                
                // Highlight search terms
                $excerpt = preg_replace('/(' . preg_quote($search_query, '/') . ')/i', '<strong>$1</strong>', $excerpt);
                
                $results[] = array(
                    'title' => $title,
                    'publication' => $publication,
                    'date' => $date,
                    'excerpt' => $excerpt,
                    'url' => $extracted_dir . '/' . $filename,
                    'pdf_url' => 'scans/' . str_replace('.html', '.pdf', $filename)
                );
            }
            
            if (count($results) >= $max_results) {
                break;
            }
        }
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search Results - Michael Giltz</title>
    <link href="giltz.css" rel="stylesheet" type="text/css" />
    <style>
        .search-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .search-form {
            text-align: center;
            margin-bottom: 30px;
        }
        .search-form input[type="text"] {
            padding: 10px 15px;
            width: 300px;
            border: 1px solid #ccc;
            border-radius: 3px;
            font-size: 16px;
        }
        .search-form button {
            padding: 10px 30px;
            background-color: #333;
            color: white;
            border: none;
            border-radius: 3px;
            cursor: pointer;
            font-size: 16px;
        }
        .search-form button:hover {
            background-color: #555;
        }
        .results-info {
            margin-bottom: 20px;
            color: #666;
        }
        .search-result {
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #eee;
        }
        .search-result h3 {
            margin: 0 0 5px 0;
        }
        .search-result .meta {
            color: #666;
            font-size: 14px;
            margin-bottom: 10px;
        }
        .search-result .excerpt {
            margin-bottom: 10px;
            line-height: 1.5;
        }
        .search-result .links a {
            margin-right: 15px;
            color: #0066cc;
        }
        .no-results {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        .back-link {
            text-align: center;
            margin-top: 30px;
        }
    </style>
</head>
<body>
    <div class="search-container">
        <h1>Search Michael Giltz Articles</h1>
        
        <div class="search-form">
            <form method="get" action="">
                <input type="text" name="q" value="<?php echo htmlspecialchars($search_query); ?>" placeholder="Search articles..." />
                <button type="submit">Search</button>
            </form>
        </div>
        
        <?php if ($search_query): ?>
            <?php if (strlen($search_query) < 3): ?>
                <div class="no-results">
                    <p>Please enter at least 3 characters to search.</p>
                </div>
            <?php elseif (count($results) > 0): ?>
                <div class="results-info">
                    Found <?php echo count($results); ?> result<?php echo count($results) > 1 ? 's' : ''; ?> for "<?php echo htmlspecialchars($search_query); ?>"
                </div>
                
                <?php foreach ($results as $result): ?>
                    <div class="search-result">
                        <h3><a href="<?php echo $result['url']; ?>"><?php echo htmlspecialchars($result['title']); ?></a></h3>
                        <div class="meta">
                            <?php echo htmlspecialchars($result['publication']); ?> • <?php echo $result['date']; ?>
                        </div>
                        <div class="excerpt">
                            <?php echo $result['excerpt']; ?>
                        </div>
                        <div class="links">
                            <a href="<?php echo $result['url']; ?>">Read Article</a>
                            <a href="<?php echo $result['pdf_url']; ?>">Download PDF</a>
                        </div>
                    </div>
                <?php endforeach; ?>
            <?php else: ?>
                <div class="no-results">
                    <p>No results found for "<?php echo htmlspecialchars($search_query); ?>"</p>
                    <p>Try different keywords or browse the categories.</p>
                </div>
            <?php endif; ?>
        <?php else: ?>
            <div class="no-results">
                <p>Enter a search term to find articles.</p>
            </div>
        <?php endif; ?>
        
        <div class="back-link">
            <a href="index.htm">← Back to Homepage</a>
        </div>
    </div>
</body>
</html>