<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TP3 - formulaire </title>
</head>
<body>
    <h2> Formulaire d'inscription </h2>
    <form method="POST" action="">
        Nom:<input type= "text" name= "nom"><br><br>
        Prénom:<input type= "text" name="prénom"><br><br>
        Age: <input type="number" name=" age"><br><br>
        Email:<input type=" text" name="email"><br><br>
        Mot de passe :<input type=" text" name="password"><br><br>
        <input type="submit" value= "Envoyer">
    </form>



     <?php
     if(isset($_POST['nom']) && isset($_POST['age'])&& isset($_POST['prénom'])&& isset($_POST['email'])&& isset($_POST['password'])) {
         $nom = trim($_POST['nom']);
         $prénom = trim($_POST['prénom']);
         $age = trim($_POST['age']);
         $email = trim($_POST['email']);
         $mot_de_passe = trim($_POST['password']);
         if(empty($nom)|| empty($age)|| empty($prénom)|| empty($email)|| empty($mot_de_passe)) {
            echo "Tous les champs sont obligatoires.";
         }
           elseif(!is_numeric($age)) {
            echo "L'âge doit être un nombre.";
           }
           else {
            echo "<h3>Données Validées :</h3>";
            echo "Nom :" .htmlspecialchars($nom). "<br>";
            echo "Prénom :" .$prénom."<br>";
            echo "Age :" .$age. "<br>";
            echo "Email :" .filter_var($email)."<br>";
            echo "Mot de passe :" .$mot_de_passe. "<br>";
           }
     }
    ?>

    
</body>
</html>