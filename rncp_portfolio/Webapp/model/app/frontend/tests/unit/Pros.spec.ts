import { render, screen } from '@testing-library/vue'
import { vi } from 'vitest'

// on fabrique un faux composant pour isoler la logique d'affichage
const Pros = {
    template: `
    <div>
      <h2>Liste des Professionnels</h2>
      <ul>
        <li v-for="pro in pros" :key="pro.id">{{ pro.firstname }} {{ pro.lastname }}</li>
      </ul>
    </div>
  `,
    props: ['pros'],
}

test('affiche la liste des pros', async () => {
    const mockPros = [
        { id: 1, firstname: 'Jean', lastname: 'Dupont' },
        { id: 2, firstname: 'Alice', lastname: 'Martin' },
    ]

    render(Pros, {
        props: { pros: mockPros },
    })

    expect(await screen.findByText(/Jean Dupont/i)).toBeTruthy()
    expect(await screen.findByText(/Alice Martin/i)).toBeTruthy()
})
