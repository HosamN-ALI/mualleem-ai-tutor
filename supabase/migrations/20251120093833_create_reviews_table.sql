/*
  # Create Reviews and Ratings System

  ## Overview
  This migration creates a comprehensive review and rating system for the RAG assistant (Mualleem platform).
  Users can rate responses and provide feedback to improve the AI assistant's performance.

  ## 1. New Tables
  
  ### `reviews`
  Stores user feedback and ratings for AI responses
  - `id` (uuid, primary key) - Unique identifier for each review
  - `user_id` (uuid, nullable) - Reference to the user who submitted the review (null for anonymous)
  - `session_id` (text, not null) - Client-side session identifier to track conversations
  - `question` (text, not null) - The original question asked by the user
  - `answer` (text, not null) - The AI-generated answer that was reviewed
  - `rating` (integer, not null) - Rating from 1-5 stars
  - `feedback` (text, nullable) - Optional text feedback from the user
  - `model_used` (text, nullable) - The AI model used to generate the answer
  - `context_used` (boolean, default false) - Whether curriculum context was used
  - `created_at` (timestamptz, default now()) - Timestamp of review submission
  - `updated_at` (timestamptz, default now()) - Last update timestamp

  ### `review_analytics`
  Aggregated statistics for admin dashboard (future feature)
  - `id` (uuid, primary key) - Unique identifier
  - `date` (date, not null, unique) - Date for the analytics
  - `total_reviews` (integer, default 0) - Total number of reviews on this date
  - `average_rating` (numeric, default 0) - Average rating for the date
  - `rating_distribution` (jsonb, default '{}') - Distribution of ratings {1: count, 2: count, etc}
  - `created_at` (timestamptz, default now()) - Creation timestamp
  - `updated_at` (timestamptz, default now()) - Last update timestamp

  ## 2. Security (RLS Policies)
  
  ### Reviews Table
  - **Public Insert**: Anyone can submit reviews (anonymous or authenticated)
  - **Public Select**: Anyone can read reviews for transparency
  - **Authenticated Update**: Only authenticated users can update their own reviews
  - **Admin Delete**: Only authenticated users can delete reviews (for moderation)

  ### Review Analytics Table
  - **Public Select**: Anyone can view aggregated statistics
  - **Service Role Only**: Only service role can insert/update analytics (automated process)

  ## 3. Indexes
  - Index on `session_id` for fast session-based queries
  - Index on `created_at` for time-based analytics
  - Index on `rating` for rating-based filtering
  - Index on `date` in review_analytics for fast lookups

  ## 4. Functions
  - Trigger function to automatically update `updated_at` timestamp

  ## 5. Important Notes
  - Reviews are allowed for anonymous users to encourage feedback
  - Session IDs are client-generated UUIDs to track conversation flows
  - Rating must be between 1 and 5 (enforced by CHECK constraint)
  - Future: Analytics table can be populated by a scheduled function
*/

-- Create reviews table
CREATE TABLE IF NOT EXISTS reviews (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES auth.users(id) ON DELETE SET NULL,
  session_id text NOT NULL,
  question text NOT NULL,
  answer text NOT NULL,
  rating integer NOT NULL CHECK (rating >= 1 AND rating <= 5),
  feedback text,
  model_used text,
  context_used boolean DEFAULT false,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create review_analytics table for future dashboard
CREATE TABLE IF NOT EXISTS review_analytics (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  date date NOT NULL UNIQUE,
  total_reviews integer DEFAULT 0,
  average_rating numeric(3,2) DEFAULT 0,
  rating_distribution jsonb DEFAULT '{}'::jsonb,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_reviews_session_id ON reviews(session_id);
CREATE INDEX IF NOT EXISTS idx_reviews_created_at ON reviews(created_at);
CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating);
CREATE INDEX IF NOT EXISTS idx_review_analytics_date ON review_analytics(date);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for reviews table
DROP TRIGGER IF EXISTS update_reviews_updated_at ON reviews;
CREATE TRIGGER update_reviews_updated_at
  BEFORE UPDATE ON reviews
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Trigger for review_analytics table
DROP TRIGGER IF EXISTS update_review_analytics_updated_at ON review_analytics;
CREATE TRIGGER update_review_analytics_updated_at
  BEFORE UPDATE ON review_analytics
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Enable Row Level Security
ALTER TABLE reviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE review_analytics ENABLE ROW LEVEL SECURITY;

-- RLS Policies for reviews table

-- Anyone can insert reviews (anonymous feedback encouraged)
CREATE POLICY "Anyone can submit reviews"
  ON reviews
  FOR INSERT
  TO anon, authenticated
  WITH CHECK (true);

-- Anyone can read reviews (public transparency)
CREATE POLICY "Anyone can read reviews"
  ON reviews
  FOR SELECT
  TO anon, authenticated
  USING (true);

-- Authenticated users can update their own reviews
CREATE POLICY "Users can update own reviews"
  ON reviews
  FOR UPDATE
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Authenticated users can delete their own reviews
CREATE POLICY "Users can delete own reviews"
  ON reviews
  FOR DELETE
  TO authenticated
  USING (auth.uid() = user_id);

-- RLS Policies for review_analytics table

-- Anyone can read analytics (public metrics)
CREATE POLICY "Anyone can read analytics"
  ON review_analytics
  FOR SELECT
  TO anon, authenticated
  USING (true);

-- Only service role can insert/update analytics (automated)
-- Note: Service role bypasses RLS, so these are just for documentation
CREATE POLICY "Service role can insert analytics"
  ON review_analytics
  FOR INSERT
  TO service_role
  WITH CHECK (true);

CREATE POLICY "Service role can update analytics"
  ON review_analytics
  FOR UPDATE
  TO service_role
  USING (true)
  WITH CHECK (true);
