import feature_extraction.collect_features as collect_features
import feature_extraction.features_per_sentence as features_per_sentence
import feature_extraction.stats as stats


def main():
    # Collect fixations happened on sentences and count fixations per sentence 
    collect_features.collect_fixations()
    features_per_sentence.fixations_per_sentence()
    
    #Collect the statistics of fixations happened on problematic words
    stats.check_fixations()
    
    # Collect jumps and count jumps per sentence 
    collect_features.collect_jumps()
    features_per_sentence.jumps_per_sentence()
    
    #Collect the statistics of jumps happened on problematic words
    stats.check_jumps()

if __name__ == "__main__":
    main()