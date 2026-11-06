import ImageUploader from "@/components/ImageUploader";

export default function Home() {
  return (
    <main>
      <h1 className="title lekton-regular">Rock 🪨 Paper 📄 Scissors ✂️</h1>
      <h2 className="muted lekton-regular">Instructions:</h2>
      <ol>
        <li className="muted lekton-regular">Choose between Rock, Paper & Scissors</li>
        <li className="muted lekton-regular">Take a picture of your hand doing that motion OR choose one online</li>
        <li className="muted lekton-regular">Upload it below</li>
        <li className="muted lekton-regular">The model will try to win by predicting the motion you did</li>
      </ol>
      <ImageUploader />
    </main>
  );
}
