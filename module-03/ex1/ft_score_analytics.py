import sys


def main() -> None:
    valid_scores = []
    print("=== Player Score Analytics ===")
    for arg in sys.argv[1:]:
        try:
            score = int(arg)
            valid_scores.append(score)
        except ValueError:
            print(f"Invalid parameter: '{arg}'")
    if len(valid_scores) == 0:
        print("No scores provided. "
              "Usage: python3 ft_score_analytics.py <score1> <score2> ...")
    else:
        print(f"Scores processed: {valid_scores}")
        print(f"Total players: {len(valid_scores)}")
        print(f"Total score: {sum(valid_scores)}")
        avg = sum(valid_scores) / len(valid_scores)
        print(f"Average score: {avg}")
        print(f"High score: {max(valid_scores)}")
        print(f"Low score: {min(valid_scores)}")
        print(f"Score range: {max(valid_scores) - min(valid_scores)}")
        print()


if __name__ == "__main__":
    main()
