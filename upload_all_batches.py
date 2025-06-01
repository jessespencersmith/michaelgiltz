#!/usr/bin/env python3
"""
Upload all article batches automatically
"""

import subprocess
import time
from datetime import datetime

def main():
    total_batches = 9
    start_time = datetime.now()
    
    print("=" * 60)
    print("Uploading all article batches")
    print("=" * 60)
    
    # Start from batch 1 since batch 0 is already done
    for batch in range(1, total_batches):
        print(f"\n🚀 Starting batch {batch + 1}/{total_batches}")
        
        try:
            # Run the batch upload script
            result = subprocess.run(
                ["python3", "upload_articles_batch.py", str(batch)],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"❌ Batch {batch} failed!")
                print(result.stderr)
                break
            
            print(f"✅ Batch {batch + 1} complete!")
            
            # Small delay between batches
            if batch < total_batches - 1:
                print("Waiting 5 seconds before next batch...")
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Upload interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Error in batch {batch}: {e}")
            break
    
    duration = datetime.now() - start_time
    print("\n" + "=" * 60)
    print("All batches processed!")
    print(f"Total duration: {duration}")
    print("\n✨ Check the live site: https://www.michaelgiltz.com")

if __name__ == "__main__":
    main()